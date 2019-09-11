from setuptools import setup, find_packages

VERSION = (0, 2, 5)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))

install_requires = [
    'aiomisc[uvloop]',
    'aiohttp',
    'peewee',
    'Marshmallow-Peewee',
    'psycopg2-binary',
    'websockets',
]

dependency_links = [
    'git+https://github.com/sammchardy/python-binance.git@feature/asyncio',
]

tests_require = [
    'pytest',
    'pytest-asyncio',
    'pytest-cov',
]

setup(
    name='common',
    description="Common tools for BB project",
    license="No License",
    version=__versionstr__,
    author="Vladas Tamoshaitis",
    packages=find_packages(
        where='.',
        exclude=('tests*',)
    ),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: AsyncIO"
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
    python_requires="~=3.5",
    tests_require=tests_require,
    extras_require={'develop': tests_require},
    #entry_points={"pytest11": ["peewee_pytest = common.pytest_peewee_plugin"]},
)
