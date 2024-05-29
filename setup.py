# -*- coding: utf-8 -*-
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='''ckanext-who-afro''',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # http://packaging.python.org/en/latest/tutorial.html#version
    version='0.0.1',

    description='''Project for CKAN customizations for the CKAN instance used in the WHO AFRO Data Hub.''',
    long_description=long_description,
    long_description_content_type="text/markdown",

    # The project's main homepage.
    url='https://github.com/fjelltopp/ckanext-who-afro',

    # Author details
    author='''Jonathan Berry''',
    author_email='''jonathan@fjelltopp.org''',

    # Choose your license
    license='AGPL',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        # 3 - Alpha
        # 4 - Beta
        # 5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.9',
    ],


    # What does your project relate to?
    keywords='''CKAN''',

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
        namespace_packages=['ckanext'],

    install_requires=[
      # CKAN extensions should not list dependencies here, but in a separate
      # ``requirements.txt`` file.
      #
      # http://docs.ckan.org/en/latest/extensions/best-practices.html
      # add-third-party-libraries-to-requirements-txt
    ],

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,
    package_data={
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see http://docs.python.org/3.4/distutils/setupscript.html
    # installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points='''
        [ckan.plugins]
        who_afro=ckanext.who_afro.plugin:WHOAFROPlugin

        [babel.extractors]
        ckan = ckan.lib.extract:extract_ckan
    ''',

    # If you are changing from the default layout of your extension, you may
    # have to change the message extractors, you can read more about babel
    # message extraction at
    # http://babel.pocoo.org/docs/messages/#extraction-method-mapping-and-configuration
    message_extractors={
        '../.minikubevenv': [
            ('**/ckanext/blob_storage/templates/resource_2.8.html', 'ignore', None),
            ('**/ckanext/scheming/2.8_templates/**', 'ignore', None),
            ('*/src/**.py', 'python', None),
            ('*/src/**.js', 'javascript', None),
            ('*/src/**.html', 'ckan', None),
        ],
        '../ckan/ckan': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**.html', 'ckan', None),
        ],
        '../ckan/ckanext': [
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**.html', 'ckan', None),
        ],
        'ckanext': [
            ('**/node_modules/**', 'ignore', None),
            ('**.py', 'python', None),
            ('**.js', 'javascript', None),
            ('**.html', 'ckan', None),
        ]
    }
)
