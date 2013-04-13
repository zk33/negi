import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="negi",
    version="0.1.0",
    author="Takaaki Yamazaki",
    author_email="ymzktkak@gmail.com",
    description="Negi is a static HTML build tool based on jinja2+JSON",
    license="MIT",
    keywords="jinja2 JSON",
    url="https://github.com/zk33/negi",
    packages=find_packages(exclude=['ez_setup', 'tests', 'tests.*']),
    long_description=read('README.md'),
    install_requires=["aaargh","jinja2"],
    entry_points={'console_scripts': ["negi = negi.main:main"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
     ],
     zip_safe=False,
)
