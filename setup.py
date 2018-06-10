from setuptools import setup, find_packages

setup(
    name="flask_uauth",
    description="Simple authentication to Flask REST apis",
    author="Panagiotis Matigakis",
    author_email="pmatigakis@gmail.com",
    version="0.1.0",
    packages=find_packages(exclude=["tests"]),
    install_requires=[
        "Flask>=0.11.1"
    ],
    tests_require=["nose"],
    test_suite="nose.collector",
    zip_safe=True
)
