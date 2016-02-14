#
"""
"""
import os
import pkg_resources

from setuptools import setup, find_packages



here = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'CHANGES.rst')) as f:
    CHANGES = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    requires = map(str, pkg_resources.parse_requirements(f.read()))


setup(
    name='pyramid_configurator',
    description='pyramid_configurator',
    version='0.0.dev0',
    long_description=README + '\n\n' + CHANGES,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        ],
    maintainer='',
    maintainer_email='',
    url='',
    keywords='pyramid configuration',
    packages=find_packages(exclude=['tests', '*.tests', '*.tests.*']),
    include_package_data=True,
    zip_safe=False,
    test_suite='tests',
    install_requires=requires,
)
