import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpt_helpers",
    version="0.1.0",
    author="Kasun Hewage",
    author_email="kasun.ch@gmail.com",
    description="Helper functions for CPT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blixttech/cpt-helpers",
    packages=setuptools.find_packages(),
    package_data={},
    entry_points = {},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        "conan-package-tools"
    ],
)
