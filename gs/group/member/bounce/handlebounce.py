# coding=utf-8
import json
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from gs.content.form import SiteForm
from gs.profile.notify.notifyuser import NotifyUser
from Products.CustomUserFolder.userinfo import IGSUserInfo
from handler import Handler, NO_NOTIFY, NOTIFY_BOUNCE, NOTIFY_DISABLED
from interfaces import IGSBounceHandler

class NoUser(Exception):
    pass

class HandleBounce(SiteForm):
    label = u'Handle a bounce'
    pageTemplateFileName = 'browser/templates/handlebounce.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSBounceHandler, render_context=False)
    
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)
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

    @form.action(label=u'Check', failure='handle_the_jandal_failure')
    def handle_the_jandal(self, action, data):
        emailAddress = data['userEmail']
        try:
            userInfo = self.user_from_email(emailAddress)
        except NoUser, nu:
            self.status = str(nu)
        else:
            groupInfo = createObject('groupserver.GroupInfo', self.site, 
                                     data['groupId'])
            handler = Handler(self.context, groupInfo)

            notifyStatus = handler.process(userInfo, emailAddress)
            if notifyStatus == NOTIFY_BOUNCE:
                self.notify_bounce(groupInfo, userInfo, emailAddress)
            elif notifyStatus == NOTIFY_DISABLED:
                self.notify_disabled(groupInfo, userInfo, emailAddress)

            self.status = u'Done'

    def handle_the_jandal_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

    def notify_bounce(self, groupInfo, userInfo, emailAddress):
        # Send a bounce notification to all the addresses that work.
        nu = NotifyUser(userInfo.user, self.siteInfo)
        addresses = nu.get_addresses()
        ea = emailAddress.lower()
        if ea in addresses:
            addresses.remove(ea)
        # TODO: convert to HTML
        nDict =  {
            'userInfo'      : userInfo,
            'groupInfo'     : groupInfo,
            'siteInfo'      : self.siteInfo,
            'supportEmail'  : self.siteInfo.get_support_email(),
            'bounced_email' : emailAddress,}
        if addresses:
            nu.send_notification('bounce_detection', n_dict = nDict,
                                 email_only = addresses)

    def notify_disabled(self, groupInfo, userInfo, emailAddress):
        nu = NotifyUser(userInfo.user, self.siteInfo)
        addresses = nu.get_addresses()
        ea = emailAddress.lower()
        if ea in addresses:
            addresses.remove(ea)
        nDict =  {
            'userInfo'      : userInfo,
            'groupInfo'     : groupInfo,
            'siteInfo'      : self.siteInfo,
            'supportEmail'  : self.siteInfo.get_support_email(),
            'bounced_email' : emailAddress,}
        if addresses:
            nu.send_notification('disabled_email', n_dict = nDict,
                                 email_only = addresses)
