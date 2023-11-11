from setuptools import setup, find_packages

setup(
    name='rks',
    version='1.0.0',
    description='rks(redis-keys-statistics) is a Python tool for analyzing and reporting key usage statistics in Redis databases, including memory usage and type distribution, created by garimoo and is under the copyright of Woowabros',
    author='garimoo',
    author_email='garimoo.kim@gmail.com',
    install_requires=['redis', 'redis-py-cluster', 'prettytable',],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'rks = rks.main:main'
        ]
    },
    keywords=['redis', 'pypi', 'redis keys statistics', 'rks', 'redis statistics', 'garim', 'garimoo'],
    python_requires='>=3.6',
    package_data={},
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)