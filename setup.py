# -*- coding: utf-8 -*-
"""setup.py for :py:module:`aiida_verdi`"""
from setuptools import setup, find_packages

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."


if __name__ == '__main__':
    setup(
        name='aiida_verdi',
        version='0.0.1',
        url='http://www.aiida.net/',
        license='MIT License',
        author="The AiiDA team",
        author_email='developers@aiida.net',
        include_package_data=True, # puts non-code files into the distribution, reads list from MANIFEST.in
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
        ],
        install_requires=['aiida', 'click', 'click-plugins', 'click-completion', 'click-spinner'],
        extras_require={
            'tests': ['pytest']
        },
        packages=find_packages(),
        entry_points={
            # following are AiiDA plugin entry points:
            'aiida.cmdline': [
                'run = aiida_verdi.commands.run:run',
                'setup = aiida_verdi.commands.setup:setup',
                'quicksetup = aiida_verdi.commands.quicksetup:quicksetup',
                'code = aiida_verdi.commands.code:code'
            ],
        },
    )
