from setuptools import setup, find_packages

setup(
    name="sorabbyngo-suid",
    version="1.0.0",
    description="Sorabbyngo Universal ID — tamper-detectable, forensically traceable entity IDs",
    author="Sorabbyngo Labs",
    author_email="eng@sorabbyngo.com",
    url="https://github.com/sorabbyngo-Labs/identity-core",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[],
    extras_require={
        "nats": ["nats-py>=2.6.0"],
        "dev":  ["pytest>=7.0", "pytest-asyncio"],
    },
    entry_points={
        "console_scripts": [
            "suid=suid.cli:main",
        ],
    },
)
