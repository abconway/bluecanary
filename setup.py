from setuptools import setup, find_packages
import os
import sys

__version__ = '0.0.4'
__requirements__ = [
    "boto3==1.2.3",
    "click==6.2",
    "pluginbase==0.3",
    "PyYAML==3.11",
]


if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload')
    sys.exit()


setup(
    name='bluecanary',
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    install_requires=__requirements__,
    entry_points='''
    [console_scripts]
    bluecanary=bluecanary.scripts.bluecanary:cli
    ''',
)
