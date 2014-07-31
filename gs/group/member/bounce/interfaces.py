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
from __future__ import unicode_literals
from zope.interface.interface import Interface
from zope.schema import ASCIILine
from gs.auth.token import AuthToken


class IGSBounceHandler(Interface):
    # TODO: Create a base email-address type
    userEmail = ASCIILine(
        title='User Email Address',
        description='The email address of the user that is bouncing',
        required=True)

    groupEmail = ASCIILine(
        title='Group Email Address',
        description='The email of the of the group that received the '
                    'bounce notification.',
        required=True)

    token = AuthToken(
        title='Token',
        description='The authentication token',
        required=True)
