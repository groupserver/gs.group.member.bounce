# -*- coding: utf-8 -*-
############################################################################
#
# Copyright © 2014 OnlineGroups.net and Contributors.
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
from __future__ import absolute_import, unicode_literals
from zope.cachedescriptors.property import Lazy
from gs.group.member.viewlet import GroupAdminViewlet
from .queries import GroupBounceQuery


class BounceLink(GroupAdminViewlet):
    'The base class for the links to the Bounces page'

    @Lazy
    def query(self):
        retval = GroupBounceQuery()
        return retval

    @Lazy
    def nBounces(self):
        retval = self.query.n_bounces_in_last_week(self.siteInfo.id,
                                                   self.groupInfo.id)
        return retval


class PastBounceLink(BounceLink):
    @Lazy
    def show(self):
        retval = (super(PastBounceLink, self).show
                  and (self.nBounces == 0))
        return retval


class RecentBounceLink(BounceLink):
    @Lazy
    def bounces(self):
        retval = self.query.get_bounces_for_group(self.siteInfo.id,
                                                  self.groupInfo.id,
                                                  limit=1)
        return retval

    @Lazy
    def show(self):
        retval = (super(RecentBounceLink, self).show
                  and (self.nBounces != 0)
                  and (self.bounces != []))
        return retval
