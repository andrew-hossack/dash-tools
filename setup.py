# -*- coding: utf-8 -*-
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

meta = {}

with open('./dash_tools/version.py') as f:
    exec(f.read(), meta)

setuptools.setup(
    name="dash-tools",
    version=meta['__version__'],
    author="Andrew Hossack",
    author_email="andrew_hossack@outlook.com",
    description="Plotly Dash Template Generator and Tools",
    download_url='https://github.com/andrew-hossack/dash-tools/archive/refs/tags/V0.4.tar.gz',
    scripts=["bin/dash-tools"],
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
    install_requires=[
        "dash==2.0.0",
        "dash-bootstrap-components==1.0.0",
        "packaging==21.0",
        "python-dotenv==0.19.2",
        "Flask==2.0.1",
        "gunicorn==20.1.0",
    ],
)
