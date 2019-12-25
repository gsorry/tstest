import io
from setuptools import find_packages, setup

with io.open("README.md", "rt", encoding="utf8") as f:
    readme = f.read()

setup(
    name='tsapp',
    version='1.0.0',
    url="https://github.com/gsorry/tstest",
    maintainer="Aleksandar Glisovic",
    maintainer_email="gsorry@gmail.com",
    description="Simple REST API based app in Flask",
    long_description=readme,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
        'flask-restful',
        'flask-httpauth',
        'flask-sqlalchemy',
        'flask-marshmallow',
        'marshmallow-sqlalchemy',
        'psycopg2-binary',
        'wtforms',
        'passlib'
    ],
    extras_require={
        "test": [
            "pytest",
            "coverage",
        ]
    },
)
