import fastentrypoints
# -*- coding: utf-8 -*-
"""setup.py for :py:module:`aiida_verdi`"""
from setuptools import setup, find_packages

__copyright__ = u"Copyright (c), This file is part of the AiiDA platform. For further information please visit http://www.aiida.net/. All rights reserved."
__license__ = "MIT license, see LICENSE.txt file."


if __name__ == '__main__':
    setup(
        name='aiida-verdi',
        version='0.1.3',
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
        setup_requires=['reentry', 'setuptools >= 18.5'],
        reentry_scan_for=['aiida.cmdline'],
        reentry_register=True,
        install_requires=['aiida', 'click', 'click-plugins', 'click-completion', 'click-spinner', 'requests'],
        extras_require={
            'tests': ['pytest']
        },
        packages=find_packages(),
        entry_points={
            'console_scripts': ['verdi-exp = aiida_verdi.cli:main'],
            # following are AiiDA plugin entry points:
            'aiida.cmdline': [
                'run = aiida_verdi.commands.run:run',
                'setup = aiida_verdi.commands.setup:setup',
                'quicksetup = aiida_verdi.commands.quicksetup:quicksetup',
                'code = aiida_verdi.commands.code:code',
                'computer = aiida_verdi.commands.computer:computer',
                'data = aiida_verdi.commands.data:data',
                'plugin = aiida_verdi.commands.plugin:plugin',
            ],
            'aiida.cmdline.code': [
                'list = aiida_verdi.commands.code.list:_list',
                'show = aiida_verdi.commands.code.show:show',
                'setup = aiida_verdi.commands.code.setup:setup'
            ],
            'aiida.cmdline.computer': [
                'setup = aiida_verdi.commands.computer.setup:setup'
            ],
            'aiida.cmdline.plugin': [
                'search = aiida_verdi.commands.plugin.search:search',
                'info = aiida_verdi.commands.plugin.info:info'
            ]
        },
    )
