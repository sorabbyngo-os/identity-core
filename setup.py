from setuptools import setup, find_packages

setup(
    name="sorabbyngo-suid",
    version="1.1.0",
    description="Sorabbyngo Universal ID system — traceable, tamper-detectable entity IDs",
    author="Sorabbyngo Company",
    author_email="dev@sorabbyngo.com",
    packages=find_packages(),
    python_requires=">=3.10",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=8.0"]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
