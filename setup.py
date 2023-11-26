from setuptools import setup, find_packages

with open("README.md","r") as readme_file:
    long_description=readme_file.read()

setup(
    name="aivr",
    version="0.0.10",
    description="Python package that integrates with Unity and provides helpful functions for users",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Waqas Kureshy",
    author_email="waqas.kureshy319@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License"
    ],
    keywords=["Unity","OpenCV","ZeroMQ"],
    packages=find_packages(),
    install_requires=[
        "numpy",
        "opencv-python",
        "pyzmq",
    ],
    python_requires=">=3.7"
)
