# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}

with open('./dashtools/version.py') as f:
    exec(f.read(), meta)

with open('requirements.txt') as f:
    requirements = f.readlines()

setuptools.setup(
    name="dash-tools",
    version=meta['__version__'],
    author="Andrew Hossack",
    author_email="andrew_hossack@outlook.com",
    description="Plotly Dash Templating and Deployment Tools",
    entry_points={
        'console_scripts': ['dashtools = dashtools.cli.cli:main']},
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrew-hossack/dash-tools",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    include_package_data=True,
    install_requires=requirements,
)
