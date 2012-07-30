# coding=utf-8
from zope.interface.interface import Interface
from zope.schema import ASCIILine, Text
from gs.auth.token import AuthToken

class IGSBounceHandler(Interface):
    # TODO: Create a base email-address type
    userEmail = ASCIILine(title=u'User Email Address',
                          description=u'The email address of the user that '\
                              u'is bouncing',
                          required=True)

    groupEmail = ASCIILine(title=u'Group Email Address',
                        description=u'The email of the of the group that '\
                            'received the bounce notification.',
                        required=True)

    token = AuthToken(title=u'Token',
                      description=u'The authentication token',
                      required=True)
