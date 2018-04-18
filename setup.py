import os
from io import open
from setuptools import setup
from setuptools import find_packages

here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst'), "r", encoding="utf-8") as fobj:
    long_description = fobj.read()

requires = [
    "psutil",    
    "dictop",
    "appserver",
]

setup(
    name="keepserver",
    version="0.2.0",
    description="Monitor keepalived status, run start.sh if server get MASTER role, and run stop.sh if server get SLAVE role.",
    long_description=long_description,
    url="https://github.com/appstore-zencore/keepserver",
    author="zencore",
    author_email="dobetter@zencore.cn",
    license="MIT",
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords=['keepserver'],
    requires=requires,
    install_requires=requires,
    packages=find_packages("src", exclude=["scripts"]),
    package_dir={"": "src"},
    scripts=["src/keepserver.py"],
    entry_points={
        'console_scripts': ['keepserver = keepserver:main']
    },
)