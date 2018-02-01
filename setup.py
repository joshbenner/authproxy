from setuptools import setup


setup(
    name='authproxy',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    description='Authenticate against identity providers with HTTP requests.',
    author='Josh Benner',
    author_email='josh@bennerweb.com',
    py_modules=['authproxy'],
    entry_points={
        'console_scripts': [
            'authproxy = authproxy:main'
        ]
    },
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ]
)
