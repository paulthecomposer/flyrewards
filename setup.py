from setuptools import setup, find_packages

setup(
    name ='flyrewards',
    version ='0.0.1',
    author='Paul Taylor',
    author_email='paulthecomposer@yahoo.com',
    description='A python package to calculate the rewards earned from air travel, specifically for British Airways',
    packages=find_packages(),
    py_modules=['flights', 'fare_classes', 'ba_rewards'],
    install_requires=['geopy', 'airportsdata'],
    keywords=['python', 'flights', 'BA', 'avios', 'tier points']
)
