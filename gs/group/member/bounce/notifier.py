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
from zope.component import getMultiAdapter
from zope.cachedescriptors.property import Lazy
from gs.core import to_ascii
from gs.profile.notify.sender import MessageSender
UTF8 = 'utf-8'


class UserBounceNotifier(object):
    'Send a bounce notification to the group member'
    textTemplateName = 'gs-group-member-bounce-bouncing.txt'
    htmlTemplateName = 'gs-group-member-bounce-bouncing.html'

    def __init__(self, group, request):
        self.context = group
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, userInfo, problemAddress, toAddresses):
        subject = 'Problems sending you posts'
        text = self.textTemplate(userInfo=userInfo, email=problemAddress)
        html = self.htmlTemplate(userInfo=userInfo, email=problemAddress)
        ms = MessageSender(self.context, userInfo)
        ms.send_message(subject, text, html, toAddresses=toAddresses)
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        self.oldContentType)


class UserDisabledNotifier(object):
    'Send an email-disabled notification to the group member'
    textTemplateName = 'gs-group-member-bounce-disabled.txt'
    htmlTemplateName = 'gs-group-member-bounce-disabled.html'

    def __init__(self, group, request):
        self.context = group
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, userInfo, problemAddress, toAddresses):
        subject = 'Email delivery problems (action required)'
        text = self.textTemplate(userInfo=userInfo, email=problemAddress)
        html = self.htmlTemplate(userInfo=userInfo, email=problemAddress)
        ms = MessageSender(self.context, userInfo)
        ms.send_message(subject, text, html, toAddresses=toAddresses)
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        self.oldContentType)


class AdminDisabledNotifier(object):
    'Send an email-disabled notification to the administrator'
    textTemplateName = 'gs-group-member-bounce-disabled-admin.txt'
    htmlTemplateName = 'gs-group-member-bounce-disabled-admin.html'

    def __init__(self, group, request):
        self.context = group
        self.request = request
        h = self.request.response.getHeader('Content-Type')
        self.oldContentType = to_ascii(h if h else 'text/html')

    @Lazy
    def textTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.textTemplateName)
        assert retval
        return retval

    @Lazy
    def htmlTemplate(self):
        retval = getMultiAdapter((self.context, self.request),
                                 name=self.htmlTemplateName)
        assert retval
        return retval

    def notify(self, userInfo, adminInfo, problemAddress):
        subject = 'Member email-delivery problems (action required)'
        text = self.textTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                 email=problemAddress)
        html = self.htmlTemplate(userInfo=userInfo, adminInfo=adminInfo,
                                 email=problemAddress)
        ms = MessageSender(self.context, adminInfo)
        ms.send_message(subject, text, html)
        self.request.response.setHeader(to_ascii('Content-Type'),
                                        self.oldContentType)
