from setuptools import setup, find_packages

setup(
    name="digkit",
    version="1.0.0",
    py_modules=["digkit"],
    packages=find_packages(),
    install_requires=[
        "pandas",
        "requests",
        "beautifulsoup",
        "python-gnupg"
    ],
    entry_points={
        "console_scripts": [
            "digkit=digkit:main",
        ],
    },
    python_requires=">=3.8",
    description="A collection of digital forensics tools and scripts.",
    author="campwill",
    url="https://github.com/campwill/digkit"
)
