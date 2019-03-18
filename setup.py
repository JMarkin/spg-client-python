from setuptools import setup, find_packages

setup(
    name='rfi_client',
    version='0.0.4',
    install_requires=['requests'],
    description='Fork of client for RFI Partner API',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Yura Markin',
    author_email='yurmarkin97@gmail.com',
    url='https://github.com/JMarkin/spg-client-python',
    keywords="spg rfi partner api",
    project_urls={
        "Original github repo": "https://github.com/RFIBANK/spg-client-python",
    },
    packages=find_packages(),
)
