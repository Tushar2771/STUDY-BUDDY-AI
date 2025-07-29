from setuptools import setup,find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()


setup(
    name="LLMOPS studybuddy",
    version="0.1",
    author="Tushar rane",
    packages=find_packages(),
    install_requires= requirements
)