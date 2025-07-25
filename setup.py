from setuptools import setup, find_packages
import os

def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="display-preset-manager",
    version="1.0.0",
    author="Steven",
    description="A Windows system tray application for managing display configuration presets",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/DisplayManager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Desktop Environment",
        "Topic :: System :: Hardware",
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "display-preset-manager=display_presets:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.json", "*.bat", "*.md"],
    },
    keywords="display monitor preset configuration windows system-tray",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/DisplayManager/issues",
        "Source": "https://github.com/yourusername/DisplayManager",
        "Documentation": "https://github.com/yourusername/DisplayManager#readme",
    },
)
