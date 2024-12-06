"""Setup tool"""

import os
import setuptools
from setuptools import setup, find_packages

setuptools.setup(
    name="trivy-html-report-andresdev4",
    version="0.1.5",
    packages=setuptools.find_packages(where="src"),
    include_package_data=True,
    install_requires=["jinja2",
                      "matplotlib",
                      "python-dateutil"],
    long_description_content_type="text/markdown",
    entry_points={
        "console_scripts": [
            "trivy-html-report=trivy_html_report_andresdev4.main:main"
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
