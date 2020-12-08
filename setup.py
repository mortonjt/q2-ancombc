# ----------------------------------------------------------------------------
# Copyright (c) 2017-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
from setuptools import setup, find_packages

import versioneer

setup(
    name="q2-ancombc",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    author="Huang Lin",
    author_email="HUL40@pitt.edu",
    description="Analysis of Microbiomes",
    license='GPLv3',
    url="http://www.bioconductor.org/packages/release/bioc/html/ANCOMBC.html",
    entry_points={
        'qiime2.plugins': ['q2-ancombc=q2_ancombc.plugin_setup:plugin']
    },
    scripts=['q2_ancombc/assets/run_ancombc.R'],
    package_data={
        "q2_ancombc": ['assets/index.html', 'citations.bib'],
    },
    zip_safe=False,
)
