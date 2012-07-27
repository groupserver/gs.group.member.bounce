# coding=utf-8
import os
from setuptools import setup, find_packages
from version import get_version

version = get_version()

setup(name='gs.group.member.bounce',
    version=version,
    description="The bounce-handling subsystem for GroupServer groups.",
    long_description=open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read(),
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Framework :: Zope2",
      "Intended Audience :: Developers",
      "License :: Other/Proprietary License",
      "Natural Language :: English",
      "Operating System :: POSIX :: Linux"
      "Programming Language :: Python",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords='user, group, member, group member, bounce, email, XVERP',
    author='Michael JasonSmith',
    author_email='mpj17@onlinegroups.net',
    url='https://source.iopen.net/groupserver/gs.group.member.bounce',
    license='ZPL',
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
        'gs.auth.token',
        'gs.content.form',
        'gs.database',
        'gs.profile.notify',
        'Products.CustomUserFolder',
        'Products.GSAuditTrail',
        'Products.GSGroup',
        'Products.XWFCore',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
)

