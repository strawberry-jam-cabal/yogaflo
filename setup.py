import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="yogaflo",
    version="0.1.1",
    author="Tobin Yehle",
    author_email="tobinyehle@gmail.com",
    description="Yoga Flow Generator",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tyehle/yogaflo",
    license="MIT",
    packages=["yogaflo"],
    package_dir={"": "src"},
    package_data={"yogaflo": ["data/poses.json", "data/flows/*.json"]},
    install_requires=["markovify"],
    entry_points={
        "console_scripts": ["yogaflo=yogaflo.__main__:console_entry"]
    },
    classifiers=[
        "Development Status :: 3 - Alpha",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Operating System :: OS Independent",

        "Environment :: Console",

        "Typing :: Typed",
    ],
)
