from setuptools import setup, find_packages

setup(
    name="digkit",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={"digkit": ["data/*.json"]},
    install_requires=[
        "pandas",
        "requests",
        "beautifulsoup4",
        "python-gnupg"
    ],
    entry_points={
        "console_scripts": [
            "digkit=digkit.cli:main",
        ],
    },
    python_requires=">=3.8",
    description="A collection of digital forensics tools and scripts.",
    author="campwill",
    url="https://github.com/campwill/digkit"
)
