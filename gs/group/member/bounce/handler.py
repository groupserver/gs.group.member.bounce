# coding=utf-8
from datetime import datetime
from zope.cachedescriptors.property import Lazy
from Products.CustomUserFolder.queries import UserQuery
from audit import BounceHandlingAuditor, BOUNCE, DISABLE
from queries import BounceQuery

NO_NOTIFY       = 0
NOTIFY_BOUNCE   = 1
NOTIFY_DISABLED = 2

class Handler(object):
    def __init__(self, site, groupId):
        self.site = self.context = site
        self.siteInfo = createObject('groupserver.SiteInfo', site)
        self.groupInfo = createObject('groupserver.GroupInfo', site, groupId)

    @Lazy
    def bounceQuery(self):
        retval = BounceQuery(self.context)
        return retval

    def process(self, userInfo, emailAddress):
        # Get the list of previous bounces.
        previousBounceDates, daysChecked = \
            self.bounceQuery.previousBounceDates(emailAddress)
        # Record the bounce
        bq.addBounce(userInfo.id, groupInfo.id, siteInfo.id, emailAddress)

        auditor = BounceHandlingAuditor(self.context, userInfo, self.groupInfo, 
                                        self.siteInfo)
        auditor.info(BOUNCE, emailAddress)
        
        retval = NO_NOTIFY
        now = datetime.now()
        bounceDate = now.strftime("%Y%m%d")
        if bounceDate not in previousBounceDates:
            previousBounceDates.append(bounceDate)
            retval = NOTIFY_BOUNCE
        
        # If the address is bouncing too much then disable it.
        numBounceDays = len(previousBounceDates)
        if numBounceDays >= 5: # TODO: make "5" an option
            self.diable_email(userInfo, emailAddress)
            stats = '%d;%d' % (numBounceDays, daysChecked)
            auditor.info(DISABLE, email, stats)
            retval = NOTIFY_DISABLED

        assert retval in (NO_NOTIFY, NOTIFY_BOUNCE, NOTIFY_DISABLED)
        return retval

    def disable_email(self, userInfo, emailAddress):
        # TODO: Move the unverify_userEmail query to this egg.
        uq = UserQuery(userInfo.user)
        uq.unverify_userEmail(emailAddress)
        assert type(shouldNotify) == bool
        return shouldNoftify
