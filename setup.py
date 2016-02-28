#
"""
"""
import os
import re
import pkg_resources

from setuptools import setup, find_packages


def read_version(fobj):
    regex = re.compile(r'^__version__\s*=\s*u?[\'"]([^\'"]+)')
    for line in fobj:
        matches = regex.match(line)
        if matches:
            return matches.group(1)

    # Else unknown version
    return 'unknown'


HERE = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(HERE, 'pyramid_configurator', '__init__.py')) as f:
    module_version = read_version(f)

with open(os.path.join(HERE, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(HERE, 'CHANGES.rst')) as f:
    CHANGES = f.read()

with open(os.path.join(HERE, 'requirements.txt')) as f:
    requires = map(str, pkg_resources.parse_requirements(f.read()))


setup(
    name='pyramid_configurator',
    description='pyramid_configurator',
    version=module_version,
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
