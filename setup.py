from setuptools import setup, find_packages

with open('requirement.txt') as fp:
    libraries = fp.read()

setup(
    name='xFlask',
    packages=find_packages(exclude=['test']),
    version='0.0.1',
    description='xFlask Restful Framework',
    author='LEANG Sotheara',
    author_email='leangsotheara@gmail.com',
    url='https://github.com/sotheara-leang/xFlask.git',
    keywords=['xFlask', 'Restful'],
    install_requires=libraries,
    python_requires=">=3.5",
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
