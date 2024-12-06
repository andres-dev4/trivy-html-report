"""Setup tool"""

import os
from setuptools import setup, find_packages
import setuptools

install_requires = open("requirements.txt").read().splitlines()



setuptools.setup(
    name="trivy_html_report",
    version="0.1.0",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "trivy-to-html=trivy_html_report.main:main",
        ],
    },
    description="CLI tool to convert Trivy JSON reports to HTML.",
    author="Andrés Antonio",
    author_email="andres.antonio.lopez@outlook.com",
    url="https://github.com/andres-dev4/trivy-html-report",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    license="MIT",
)
