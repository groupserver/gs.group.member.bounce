# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2012, 2013, 2014 OnlineGroups.net and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
############################################################################
import codecs
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

with codecs.open('README.txt', encoding='utf-8') as f:
    long_description = f.read()
with codecs.open(os.path.join("docs", "HISTORY.txt"),
                 encoding='utf-8') as f:
    long_description += '\n' + f.read()

setup(name='gs.group.member.bounce',
      version=version,
      description="The bounce-handling subsystem for GroupServer groups.",
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          "Environment :: Web Environment",
          "Framework :: Zope2",
          "Intended Audience :: Developers",
          'License :: OSI Approved :: Zope Public License',
          "Natural Language :: English",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: Implementation :: CPython",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='user, group, member, group member, bounce, email, XVERP',
      author='Michael JasonSmith',
      author_email='mpj17@onlinegroups.net',
      url='https://source.iopen.net/groupserver/gs.group.member.bounce',
      license='ZPL 2.1',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['gs', 'gs.group', 'gs.group.member'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'pytz',
          'sqlalchemy',
          'zope.cachedescriptors',
          'zope.component',
          'zope.formlib',
          'zope.interface',
          'zope.schema',
          'zope.sqlalchemy',
          'zope.tal',
          'zope.tales',
          'zope.viewlet',
          'Zope2',
          'gs.auth.token',
          'gs.database',
          'gs.group.member.info',
          'gs.group.member.viewlet',
          'gs.group.messages.add.base',
          'gs.profile.base',
          'gs.profile.notify',
          'Products.GSContent',
          'Products.CustomUserFolder',
          'Products.GSAuditTrail',
          'Products.GSGroup',
          'Products.XWFCore',
      ],
      entry_points="""
          # -*- Entry points: -*-
      """,)
