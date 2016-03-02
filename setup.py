# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
import os

version = '1.0dev0'
shortdesc = 'Github Organization Information and Management Tools'
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()
longdesc = open(os.path.join(os.path.dirname(__file__), 'CHANGES.rst')).read()

setup(
    name='plone.github',
    version=version,
    description=shortdesc,
    long_description=longdesc,
    classifiers=[
        "Programming Language :: Python",
    ],
    keywords='python plone github',
    author='Jens W. Klein',
    author_email='jens@bluedynamics.com',
    url=u'https://pypi.python.org/pypi/plone.github',
    license='GPL 2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    namespace_packages=['plone'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'PyGithub',
    ],

    extras_require={
        'dev': [
            'ipdb',
        ],
    },
    entry_points="""\
    [console_scripts]
    manage_labels = plone.github.labels:manage_labels
    """,
)
