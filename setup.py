import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="MLAnimator",
    version="0.0.1",
    author="Hoversquid",
    author_email="contactprojectworldmap@gmail.com",
    description="Sorts and animates the output of Machine Learning image rendering programs.",
    long_description=long_description,
    url="https://github.com/Hoversquid/MLAnimator/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
