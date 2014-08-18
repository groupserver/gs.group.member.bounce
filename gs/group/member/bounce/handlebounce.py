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
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from gs.group.messages.add.base import ListInfoForm
from gs.profile.email.base import EmailUser
from Products.CustomUserFolder.userinfo import IGSUserInfo
from .handler import Handler, NOTIFY_BOUNCE, NOTIFY_DISABLED
from .interfaces import IGSBounceHandler
from .notifier import (UserBounceNotifier, UserDisabledNotifier,
                       AdminDisabledNotifier)


class NoUser(Exception):
    pass


class HandleBounce(ListInfoForm):
    label = 'Handle a bounce'
    pageTemplateFileName = 'browser/templates/handlebounce.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSBounceHandler, render_context=False)

    def __init__(self, context, request):
        ListInfoForm.__init__(self, context, request)
        self.site = context

    @Lazy
    def acl_users(self):
        retval = self.context.acl_users
        return retval

    def user_from_email(self, emailAddress):
        user = self.acl_users.get_userByEmail(emailAddress)
        if not user:
            m = 'No user found for %s' % emailAddress
            raise NoUser(m)
            assert False, "Figure out what to do."
        retval = IGSUserInfo(user)
        return retval

    def site_from_email(self, email):
        site_root = self.context.site_root()
        content = site_root.Content
        siteId = self.get_site_id(email)
        retval = getattr(content, siteId)
        return retval

    def groupInfo_from_email(self, site, email):
        groupId = self.get_group_id(email)
        retval = createObject('groupserver.GroupInfo', site, groupId)
        return retval

    @form.action(label='Handle', failure='handle_the_jandal_failure')
    def handle_the_jandal(self, action, data):
        emailAddress = data['userEmail']
        try:
            userInfo = self.user_from_email(emailAddress)
        except NoUser as nu:
            self.status = str(nu)
        else:
            site = self.site_from_email(data['groupEmail'])
            groupInfo = self.groupInfo_from_email(site, data['groupEmail'])
            handler = Handler(site, groupInfo)

            notifyStatus = handler.process(userInfo, emailAddress)
            if notifyStatus == NOTIFY_BOUNCE:
                self.notify_bounce(groupInfo, userInfo, emailAddress)
            elif notifyStatus == NOTIFY_DISABLED:
                self.notify_disabled(groupInfo, userInfo, emailAddress)
                self.admin_notify_disabled(groupInfo, userInfo,
                                           emailAddress)

            self.status = 'Done'

    def handle_the_jandal_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = '<p>There is an error:</p>'
        else:
            self.status = '<p>There are errors:</p>'

    def notify_bounce(self, groupInfo, userInfo, emailAddress):
        'Send a bounce notification to all the addresses that work.'
        eu = EmailUser(self.context, userInfo)
        lea = emailAddress.lower()
        lAddresses = [a.lower() for a in eu.get_addresses()]
        if lea in lAddresses:
            lAddresses.remove(lea)

        if lAddresses:
            ubn = UserBounceNotifier(groupInfo.groupObj, self.request)
            ubn.notify(userInfo, emailAddress, lAddresses)

    def notify_disabled(self, groupInfo, userInfo, emailAddress):
        'Send a disabled notification to all the addresses that work.'
        eu = EmailUser(self.context, userInfo)
        lea = emailAddress.lower()
        lAddresses = [a.lower() for a in eu.get_addresses()]
        if lea in lAddresses:
            lAddresses.remove(lea)

        if lAddresses:
            udn = UserDisabledNotifier(groupInfo.groupObj, self.request)
            udn.notify(userInfo, emailAddress, lAddresses)

    def admin_notify_disabled(self, groupInfo, userInfo, emailAddress):
        'Tell the administrators that the email address has been disabled.'
        adn = AdminDisabledNotifier(groupInfo.groupObj, self.request)
        for adminInfo in groupInfo.group_admins:
            if adminInfo.id != userInfo.id:
                adn.notify(userInfo, adminInfo, emailAddress)
