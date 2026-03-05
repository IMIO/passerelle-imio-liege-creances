from setuptools import setup, find_packages

version = "0.0.1"

setup(
    name="passerelle-imio-liege-creances",
    version=version,
    author="iMio",
    author_email="support-ts@imio.be",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Environment :: Web Environment",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.11",
    ],
    url="https://github.com/IMIO/passerelle-imio-liege-creances",
    install_requires=[
        "django>=4.2",
    ],
    zip_safe=False,
)
