from setuptools import find_packages, setup

setup(
    name='notes',
    version='0.0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
        'Flask-SQLAlchemy',
        'flask-restful',
        'Flask-HTTPAuth',
        'flask-wtf',
        'email_validator',
    ],
)