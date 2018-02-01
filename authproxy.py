import sys
import argparse
import signal
import base64
import abc

from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn


def parse_comma_list(text):
    if text is None:
        return None
    return [s.strip() for s in text.split(',')]


class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in separate threads."""


class RequestHandler(BaseHTTPRequestHandler):
    providers = []

    def do_GET(self):
        auth_header = self.headers.get('Authorization')
        if auth_header is not None and auth_header.lower().startswith('basic '):
            creds = base64.b64decode(auth_header[6:]).decode('utf-8')
            username, password = creds.split(':', 1)
            authenticated = False
            for provider in self.providers:
                if provider.authenticate(username, password, self.headers):
                    authenticated = True
                    break
            self.send_response(200 if authenticated else 403)
        self.end_headers()


class Provider(abc.ABC):
    def __init__(self, config):
        self.config = config

    @abc.abstractmethod
    def authenticate(self, username, password, headers):
        pass


class LDAPProvider(Provider):
    @staticmethod
    def _parse_constraints(headers):
        return {
            'require_users': parse_comma_list(
                headers.get('AuthProxy-Require-Users')),
            'require_groups': parse_comma_list(
                headers.get('AuthProxy-Require-Groups'))
        }

    def authenticate(self, username, password, headers):
        constraints = self._parse_constraints(headers)
        return True


AUTH_PROVIDERS = {
    'ldap': LDAPProvider,
    'ldaps': LDAPProvider
}


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def exit_gracefully(signal, frame):
    sys.exit(0)


def arg_parser():
    desc = 'Simple HTTP server to proxy authentication requests.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-b', '--bind', dest='bind', metavar='IP:PORT',
                        help='IP and port to bind to',
                        default='127.0.0.1:8018')
    parser.add_argument('-u', '--uri', dest='uris', metavar='URI',
                        action='append', required=True,
                        help='URI of authentication server (multiple)')
    return parser


def main():
    parser = arg_parser()
    args = parser.parse_args()
    signal.signal(signal.SIGINT, exit_gracefully)

    providers = []
    for uri in args.uris:
        provider_name = uri.partition('://')[0]
        try:
            provider = AUTH_PROVIDERS[provider_name]
        except KeyError:
            eprint('Unknown provider: {}'.format(provider_name))
            valid = AUTH_PROVIDERS.keys()
            eprint('Valid providers: {}'.format(', '.join(valid)))
            return 1
        providers.append(provider(args))

    ip, port = args.bind.split(':')
    print('Listening on {}:{}'.format(ip, port))
    RequestHandler.providers = providers
    server = ThreadedHTTPServer((ip, int(port)), RequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    sys.exit(main())
