from setuptools import setup, find_packages


setup(
    name='bluecanary',
    version='0.0.3',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Boto3',
        'Click',
        'pluginbase',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        bluecanary=bluecanary.scripts.bluecanary:cli
    ''',
)

