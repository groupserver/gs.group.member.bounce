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
from zope.component import createObject
from gs.group.base import GroupPage
from .queries import GroupBounceQuery


class GroupBounces(GroupPage):

    def __init__(self, context, request):
        super(GroupBounces, self).__init__(context, request)

    @Lazy
    def query(self):
        retval = GroupBounceQuery()
        return retval

    @Lazy
    def bounces(self):
        bounces = self.query.get_bounces_for_group(self.siteInfo.id,
                                                   self.groupInfo.id)
        retval = []
        for bounce in bounces:
            bounce['user'] = createObject('groupserver.UserFromId',
                                          self.context, bounce['user_id'])
            retval.append(bounce)
        return retval
