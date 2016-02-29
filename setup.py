from setuptools import setup, find_packages

__version__ = '0.0.4'
__requirements__ = [
    "boto3==1.2.3",
    "click==6.2",
    "pluginbase==0.3",
    "PyYAML==3.11",
]


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
