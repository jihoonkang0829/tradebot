import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tradebot",
    version="0.0.1",
    author="Jihoon Kang, Jinpyo Lee",
    author_email="jihoonkang0829@gmail.com, kevinjplee197@gmail.com",
    description="A trading bot module for Binance Futures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jihoonkang0829/tradebot",
    project_urls={
        "Bug Tracker": "https://github.com/jihoonkang0829/tradebot/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)