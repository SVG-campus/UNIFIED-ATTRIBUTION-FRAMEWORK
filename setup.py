from setuptools import setup, find_packages

setup(
    name="unified-attribution-framework",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Unified Attribution Framework combining game theory, causality, and privacy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/username/unified-attribution-framework",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy>=1.21.0",
        "pandas>=1.3.0",
        "scipy>=1.7.0",
        "matplotlib>=3.4.0",
        "seaborn>=0.11.0",
        "scikit-learn>=1.0.0",
        "networkx>=2.6.0",
    ],
    extras_require={
        "gpu": ["torch>=1.10.0"],
        "dev": ["pytest>=6.2.0", "black>=21.0", "flake8>=3.9.0"],
    },
)
