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
from textwrap import fill
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.content.email.base import (GroupEmail, TextMixin)
UTF8 = 'utf-8'


class NotifyBounce(GroupEmail):

    def __init__(self, group, request):
        super(NotifyBounce, self).__init__(group, request)
        self.group = group
        self.email = self.siteInfo.get_support_email()

    @Lazy
    def mailingList(self):
        retval = createObject('groupserver.MailingListInfo', self.group)
        return retval

    @Lazy
    def groupEmail(self):
        retval = self.mailingList.get_property('mailto', '@')
        return retval

    def get_support_email(self, user, email):
        subj = 'Bouncing email'
        uu = '{0}{1}'.format(self.siteInfo.url, user.url)
        msg = '''I got a message saying that a post from the group
"{group}" <{groupUrl}> to my email address <{email}> could not be
delivered, and...'''
        b = msg.format(group=self.groupInfo.name, email=email,
                       groupUrl=self.groupInfo.url)
        fb = fill(b, width=74)
        body = '''Hello,

{b}

Thanks,
    {userName}
    <{userUrl}>'''.format(b=fb, userUrl=uu, userName=user.name)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.email, subj=quote(subj),
                          body=quote(body.encode(UTF8)))
        return retval


class NotifyBounceText(NotifyBounce, TextMixin):

    def __init__(self, group, request):
        super(NotifyBounceText, self).__init__(group, request)
        filename = 'bounce-from-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)
