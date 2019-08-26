from setuptools import setup, find_packages


VERSION = (0, 2, 0)
__version__ = VERSION
__versionstr__ = '.'.join(map(str, VERSION))


install_requires = [
    'aiohttp',
    'peewee',
    'Marshmallow-Peewee',
    'psycopg2-binary'
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
        exclude=('tests*', )
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
    python_requires="~=3.5",
    tests_require=tests_require,
    extras_require={'develop': tests_require},
    entry_points = {"pytest11": ["peewee_pytest = common.pytest_peewee_plugin"]},
)
