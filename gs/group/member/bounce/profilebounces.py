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
from gs.profile.base import ProfilePage
from .queries import ProfileBounceQuery


class ProfileBounces(ProfilePage):

    def __init__(self, context, request):
        super(ProfileBounces, self).__init__(context, request)

    @Lazy
    def query(self):
        retval = ProfileBounceQuery()
        return retval

    @Lazy
    def bounces(self):
        bounces = self.query.get_bounces_for_person(self.siteInfo.id,
                                                    self.userInfo.id)
        retval = []
        for bounce in bounces:
            bounce['group'] = createObject('groupserver.GroupInfo',
                                           self.context, bounce['group_id'])
            retval.append(bounce)
        return retval
