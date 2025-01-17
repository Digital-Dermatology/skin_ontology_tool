from setuptools import setup, find_packages

setup(
    name='skin_ontology_tool',
    version='0.1.0',
    description='A tool to standardize skin datasets using ICD-10 and ICD-11 ontologies.',
    author='Philippe Gottfrois',
    author_email='philippe.gottfrois@unibas.ch',
    packages=find_packages(),
    install_requires=['pandas'],
    entry_points={
        'console_scripts': [
            'skin_ontology_tool=skin_ontology_tool.main:main',
        ],
    },
    include_package_data=True,
)