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
import datetime
from pytz import UTC
import sqlalchemy as sa
from zope.sqlalchemy import mark_changed
from gs.database import getTable, getSession
from .audit import SUBSYSTEM, DISABLE
LAST_NUM_DAYS = 60


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
            in the past LAST_NUM_DAYS, or since the address was last
            disabled.
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
        s.append_whereclause(bt.c.email == email)
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
#          AND instance_user_id = userId
#          AND instance_datum = email
#        ORDER BY event_date DESC;
# Opted to leave this out instance_user_id  for reasons of efficiency.
        s = sa.select([at.c.event_date], order_by=sa.desc(at.c.event_date))
        s.append_whereclause(at.c.subsystem == SUBSYSTEM)
        s.append_whereclause(at.c.event_code == DISABLE)
        s.append_whereclause(at.c.instance_datum == email)

        retval = None

        session = getSession()
        r = session.execute(s).fetchone()

        if r:
            retval = r['event_date']
        return retval


class GroupBounceQuery(object):
    def __init__(self):
        self.bounceTable = getTable('bounce')

    @staticmethod
    def map_x(x, items):
        retval = {i: x[i] for i in items}
        return retval

    def get_bounces_for_group(self, siteId, groupId, limit=100):
        bt = self.bounceTable

        s = bt.select(order_by=sa.desc(bt.c.date), limit=limit)
        s.append_whereclause(bt.c.site_id == siteId)
        s.append_whereclause(bt.c.group_id == groupId)

        session = getSession()
        r = session.execute(s)

        m = ['site_id', 'group_id', 'user_id', 'email', 'date']
        retval = [self.map_x(x, m) for x in r]

        assert type(retval) == list
        return retval

    def n_bounces_in_last_week(self, siteId, groupId):
        bt = self.bounceTable

        cols = [sa.func.count()]
        s = sa.select(cols)
        s.append_whereclause(bt.c.site_id == siteId)
        s.append_whereclause(bt.c.group_id == groupId)
        now = datetime.datetime.now(UTC)
        lastWeek = (now - datetime.timedelta(7))
        s.append_whereclause(bt.c.date >= lastWeek)

        session = getSession()
        r = session.execute(s)
        retval = r.scalar()
        if retval is None:
            retval = 0

        assert retval >= 0
        return retval


class ProfileBounceQuery(GroupBounceQuery):
    'Like the GroupBounceQuery, but for people'

    def get_bounces_for_person(self, siteId, userId, limit=100):
        bt = self.bounceTable

        s = bt.select(order_by=sa.desc(bt.c.date), limit=limit)
        s.append_whereclause(bt.c.site_id == siteId)
        s.append_whereclause(bt.c.user_id == userId)

        session = getSession()
        r = session.execute(s)

        m = ['site_id', 'group_id', 'user_id', 'email', 'date']
        retval = [self.map_x(x, m) for x in r]

        assert type(retval) == list
        return retval

    def n_bounces_in_last_week(self, siteId, userId):
        bt = self.bounceTable

        cols = [sa.func.count()]
        s = sa.select(cols)
        s.append_whereclause(bt.c.site_id == siteId)
        s.append_whereclause(bt.c.user_id == userId)
        now = datetime.datetime.now(UTC)
        lastWeek = (now - datetime.timedelta(7))
        s.append_whereclause(bt.c.date >= lastWeek)

        session = getSession()
        r = session.execute(s)
        retval = r.scalar()
        if retval is None:
            retval = 0

        assert retval >= 0
        return retval