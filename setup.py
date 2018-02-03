from setuptools import setup


setup(
    name='httpauthproxy',
    install_requires=[
        'ldap3>=2.4,<3'
    ],
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    description='Authenticate against identity providers with HTTP requests.',
    author='Josh Benner',
    author_email='josh@bennerweb.com',
    url='https://github.com/joshbenner/httpauthproxy',
    py_modules=['httpauthproxy'],
    entry_points={
        'console_scripts': [
            'httpauthproxy = httpauthproxy:main'
        ]
    },
    license='MIT',
    keywords=['nginx', 'ldap', 'authentication'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
