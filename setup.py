from setuptools import setup, find_packages

with open('requirement.txt') as fp:
    libraries = fp.read()

setup(
    name='xFlask',
    version='0.0.1',
    description='xFlask Restful Framework',
    packages=find_packages(exclude=['test']),
    python_requires=">=3.5",
    install_requires=libraries,
    include_package_data=True
)
