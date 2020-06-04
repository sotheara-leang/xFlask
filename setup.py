from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

def requirement():
    return [
        'Flask',
        'Flask-Script',
        'Flask-Migrate',
        'Flask-SQLAlchemy',
        'Flask-Testing',
        'Flask-Injector',
        'Flask-JWT-Extended',
        'Flask-WTF',
        'WTForms',
        'email-validator',
        'Werkzeug==0.16.1',
        'PyYAML',
        'psycopg2-binary'
    ]

setup(
    name='xFlask',
    packages=find_packages(),
    package_data={'xflask': ['conf/*']},
    version='0.1.7',
    description='Python Web Framework',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='LEANG Sotheara',
    author_email='leangsotheara@gmail.com',
    url='https://github.com/sotheara-leang/xFlask.git',
    keywords=['xFlask', 'Restful', 'Web'],
    install_requires=requirement(),
    python_requires=">=3.5",
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License'
    ]
)
