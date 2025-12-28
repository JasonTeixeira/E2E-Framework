"""
Enterprise E2E Test Automation Framework
A production-ready, scalable test automation framework built with Selenium and Pytest
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="qa-automation-framework",
    version="1.0.0",
    author="Jason Teixeira",
    author_email="sage@sageideas.org",
    description="Enterprise-grade E2E test automation framework with Selenium, Pytest, and advanced features",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JasonTeixeira/Qa-Automation-Project",
    packages=find_packages(exclude=["tests*", "docs*"]),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.16.0",
        "pytest>=7.4.3",
        "pytest-xdist>=3.5.0",
        "pytest-rerunfailures>=13.0",
        "allure-pytest>=2.13.2",
        "webdriver-manager>=4.0.1",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "requests>=2.31.0",
        "loguru>=0.7.2",
        "faker>=22.0.0",
        "pillow>=10.1.0",
    ],
    extras_require={
        "dev": [
            "black>=23.12.1",
            "pylint>=3.0.3",
            "mypy>=1.7.1",
            "pytest-cov>=4.1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "qa-test=framework.cli:main",
        ],
    },
)
