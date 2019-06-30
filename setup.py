import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="colorstats",
    version="1.0.0",
    author="Nicholas Ramkissoon",
    description="Package for processing color data from images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nramkissoon/ColorStats",
    packages=setuptools.find_packages(),
    classifiers=[
        'Intended Audience :: Developers'
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)