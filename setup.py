from setuptools import setup, find_packages


setup(
    name='bluecanary',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Boto3',
        'Click',
        'coverage',
        'flake8',
        'nose',
        'pluginbase',
        'PyYAML',
    ],
    entry_points='''
        [console_scripts]
        bluecanary=bluecanary.scripts.bluecanary:cli
    ''',
)

