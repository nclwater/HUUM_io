import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="huum_io-SBerendsen", # Replace with your own username
    version="1.0.0",
    author="Sven Berendsen",
    author_email="s.berendsen2@newcastle.ac.uk",
    description="IO emthods for the Household Utility Usage Model",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/LeoTolstoi/huum_io/",
    project_urls={
        "Bug Tracker": "https://gitlab.com/LeoTolstoi/huum_io/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache 2.0 License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    # packages=['huum_io', 'huum_io.elements', 'huum_io.events', 'huum_io.translators', 'huum_io.util'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
