# coding=utf-8
import datetime
from pytz import UTC
import sqlalchemy as sa
from sqlalchemy.exc import NoSuchTableError
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession

class BounceQuery(object):
    
    def __init__(self):
        self.bounceTable = getTable('bounce')
        self.auditEventTable = getTable('audit_event')

    def addBounce(self, userId, groupId, siteId, email):
        bt = self.bounceTable
        i = bt.insert()
        now = datetime.datetime.now()
        session = getSession()
         
        session.execute(i, params={'date': now, 'user_id': userId,
                                   'group_id': groupId, 
                                   'site_id': siteId, 'email': email})
        mark_changed(session)
        
    def previousBounceDates(self, email):
        """ Checks for the number of bounces from this email address
            in the past LAST_NUM_DAYS, or since the address was last disabled. 
        """
        now = datetime.datetime.now(UTC)
        dateToCheck = (now-datetime.timedelta(LAST_NUM_DAYS))
        lastDisabledDate = self.lastDisabledDate(email)
        if lastDisabledDate: 
            lastDisabledDate = lastDisabledDate.replace(tzinfo=UTC)
            if lastDisabledDate > dateToCheck:
                dateToCheck = lastDisabledDate
        daysChecked = (now.date() - dateToCheck.date()).days
        
        bt = self.bounceTable
        s = bt.select(order_by=sa.desc(bt.c.date))
        s.append_whereclause(bt.c.email==email)
        s.append_whereclause(bt.c.date > dateToCheck)
        
        session = getSession()
        r = session.execute(s)

        bounces = []
        if r.rowcount:
            for row in r:
                bounceDate = row['date'].strftime("%Y%m%d")
                if bounceDate not in bounces:
                    bounces.append(bounceDate)
        
        return (bounces, daysChecked)

    def lastDisabledDate(self, email):
        """ Checks for the last time this address was disabled, if ever.
        """
        at = self.auditEventTable
#        SELECT event_date
#        FROM audit_event 
#        WHERE subsystem = 'groupserver.BounceHandling' AND event_code = '2'
#          AND instance_user_id = userId  # Opted to leave this out for reasons of efficiency.
#          AND instance_datum = email
#        ORDER BY event_date DESC;
        s = sa.select([at.c.event_date], order_by=sa.desc(at.c.event_date))
        s.append_whereclause(at.c.subsystem==SUBSYSTEM)
        s.append_whereclause(at.c.event_code==DISABLE)
        s.append_whereclause(at.c.instance_datum==email)
        
        retval = None        
        
        session = getSession()
        r = session.execute(s).fetchone()

        if r:
            retval = r['event_date']
        return retval
