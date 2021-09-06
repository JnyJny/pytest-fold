from io import open

from setuptools import setup, find_packages

with open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="pytest-fold2",
    entry_points={"pytest11": ["pytest_fold2 = pytest_fold2.plugin"]},
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    platforms="any",
    python_requires=">=3.5",
    install_requires=["pytest>=5.2"],
    use_scm_version={"write_to": "src/pytest_fold2/_version.py"},
    setup_requires=["setuptools_scm"],
    url="https://github.com/pytest-dev/pytest-fold",
    license="MIT",
    author="Jeff Wright",
    author_email="jeff.washcloth@gmail.com",
    description="Fold failed pytest output in console for eassier investigation",
    long_description=readme,
    keywords="pytest",
    # extras_require={"dev": ["pre-commit", "tox"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Testing",
    ],
)
