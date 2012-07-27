# coding=utf-8
import json
from zope.component import createObject
from zope.cachedescriptors.property import Lazy
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from gs.auth.token import log_auth_error
from gs.content.form import SiteForm
from interfaces import IGSBounceHandler

class HandleBounce(SiteForm):
    label = u'Handle a bounce'
    pageTemplateFileName = 'browser/templates/handlebounce.pt'
    template = ZopeTwoPageTemplateFile(pageTemplateFileName)
    form_fields = form.Fields(IGSBounceHandler, render_context=False)
    
    def __init__(self, context, request):
        SiteForm.__init__(self, context, request)

    @form.action(label=u'Check', failure='handle_the_jandal_failure')
    def handle_the_jandal(self, action, data):

        self.status = u'Done'
        return retval

    def handle_the_jandal_failure(self, action, data, errors):
        log_auth_error(self.context, self.request, errors)
        if len(errors) == 1:
            self.status = u'<p>There is an error:</p>'
        else:
            self.status = u'<p>There are errors:</p>'
        assert type(self.status) == unicode
