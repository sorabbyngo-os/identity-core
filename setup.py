from setuptools import setup, find_packages

setup(
    name="sorabbyngo-suid",
    version="1.0.0",
    description="Sorabbyngo Universal ID system",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest"]
    },
)
