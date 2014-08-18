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
from textwrap import TextWrapper
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote
from zope.cachedescriptors.property import Lazy
from zope.component import createObject
from gs.content.email.base import (GroupEmail, TextMixin)
UTF8 = 'utf-8'


# The normal bounce notification


class NotifyBounce(GroupEmail):
    supportMsgWrap = TextWrapper(width=74)

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
        fb = self.supportMsgWrap.fill(b)
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


# The Disabled email address notification


class NotifyDisabled(NotifyBounce):
    def get_support_email(self, user, email):
        subj = 'Disabled email'
        uu = '{0}{1}'.format(self.siteInfo.url, user.url)
        msg = '''I got a message saying that email address <{email}>
has been disabled, because of returned posts from "{group}" <{groupUrl}>
and...'''
        b = msg.format(group=self.groupInfo.name, email=email,
                       groupUrl=self.groupInfo.url)
        fb = self.supportMsgWrap.fill(b)
        body = '''Hello,

{b}

Thanks,
    {userName}
    <{userUrl}>'''.format(b=fb, userUrl=uu, userName=user.name)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.email, subj=quote(subj),
                          body=quote(body.encode(UTF8)))
        return retval


class NotifyDisabledText(NotifyDisabled, TextMixin):

    def __init__(self, group, request):
        super(NotifyDisabledText, self).__init__(group, request)
        filename = 'disabled-from-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)


# The Disabled email address notification to a group administrator


class NotifyAdminDisabled(NotifyBounce):
    def get_support_email(self, admin, user, email):
        subj = 'Disabled member email'
        uu = '{0}{1}'.format(self.siteInfo.url, user.url)
        au = '{0}{1}'.format(self.siteInfo.url, admin.url)
        msg = '''I got a message saying that email address <{email}>
of my group member {user} <{userUrl}> has been disabled, because of
returned posts from my group "{group}" <{groupUrl}> and...'''
        b = msg.format(group=self.groupInfo.name, email=email,
                       user=user.name, userUrl=uu,
                       groupUrl=self.groupInfo.url)
        fb = self.supportMsgWrap.fill(b)
        body = '''Hello,

{b}

Thanks,
    {adminName}
    <{adminUrl}>'''.format(b=fb, adminUrl=au, adminName=admin.name)
        m = 'mailto:{to}?Subject={subj}&body={body}'
        retval = m.format(to=self.email, subj=quote(subj),
                          body=quote(body.encode(UTF8)))
        return retval


class NotifyAdminDisabledText(NotifyAdminDisabled, TextMixin):
    indentWrapper = TextWrapper(width=74, initial_indent='    ',
                                subsequent_indent='    ')
    indentBulletWrapper = TextWrapper(width=74, initial_indent='    * ',
                                      subsequent_indent='      ')

    def __init__(self, group, request):
        super(NotifyAdminDisabled, self).__init__(group, request)
        filename = 'admin-disabled-from-{0}.txt'.format(self.groupInfo.id)
        self.set_header(filename)

    @classmethod
    def indent_fill(cls, mesg):
        retval = cls.indentWrapper.fill(mesg)
        return retval

    @classmethod
    def indent_bullet_fill(cls, mesg):
        retval = cls.indentBulletWrapper.fill(mesg)
        return retval