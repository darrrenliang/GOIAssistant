import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="goiassistant",
    version="1.1.1",
    author="Darren Liang",
    author_email="darren.liang@acspower.com",
    install_requires=["cx-Oracle", "PyQt5"],
    description="goiassistant",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={
        '': ['*.png', '*.txt']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
