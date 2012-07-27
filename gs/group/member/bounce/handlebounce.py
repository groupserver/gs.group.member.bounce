# coding=utf-8
import json
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from gs.content.form import SiteForm
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
            userInfo = user_from_email(emailAddress)
        except NoUser, nu:
            self.status = str(nu)
        else:
            handler = Handler(self.context, data['groupId'])

            notifyStatus = handler.process(userInfo, emailAddress)
            if notifyStatus == NOTIFY_BOUNCE:
                self.notify_bounce(userInfo, emailAddress)
            elif notifyStatus == NOTIFY_DISABLED:
                self.notify_disabled(userInfo, emailAddress)

            self.status = u'Done'

    def handle_the_jandal_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode

    def notify_bounce(self, userInfo, emailAddress):
        assert False, 'Should notify someone of the bounce'

    def notify_disabled(self, userInfo, emailAddress):
        assert False, 'should notify someone of the disabled'
