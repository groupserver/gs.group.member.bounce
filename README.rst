==========================
``gs.group.member.bounce``
==========================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Bouncing email reporting for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-07-31
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.Net`_.

Introduction
============

Email addresses are unreliable. Because of this SMTP servers have a way of
communicating *back* to the sender when an email message cannot be
delivered. These messages are known as **bounces**. This product
(``gs.group.member.bounce``) provides the system that allows GroupServer_
to respond to these bounces.

In this document I discuss `how bouncing works`_, and how this product will
`register a bounce`_.

How Bouncing Works
==================

An email message has two addresses in the **envelope:** a ``To`` address
and a ``From`` address.  The addresses in the **envelope** are different
from the myriad of the ``To`` and ``From`` addresses in the header of the
email messages themselves (but the envelope addresses will *usually* be
*one* of the addresses in the message-header). The envelope addresses are
set when communicating with the SMTP server [#email]_::

  ┌Envelope──────────┐
  │  To:…            │
  │  From:…          │
  │┌Message─────────┐│
  ││┌Header────────┐││
  │││    To:…      │││
  │││    CC:…      │││
  │││    BCC:…     │││
  │││    From:…    │││
  │││    Reply-To:…│││
  │││    Sender:…  │││
  ││└──────────────┘││
  ││┌Body──────────┐││
  ││└──────────────┘││
  │└────────────────┘│
  └──────────────────┘

The **VERP** system, which this product supports, allows an SMTP server to
report a bounce. If the server cannot deliver a message it will send the
message back. The ``To`` address in the envelope of the returned message is
made from the original ``To`` and ``From`` addresses::

   listId+userMailbox=user.domain@this.server

``listID``:
  The identifier of the list that sent the original email message.

``userMailbox``:
  The mail-box (left-hand side of the ``@``) that is bouncing.

``user.domain``:
  The domain of the mail-server that generated the bounce-message.

``this.server``:
  The domain of the server that sent the original email message.

From these four elements the original ``To`` and ``From`` addresses can be
re-constructed:

* User Address ``userMailbox@user.domain``
* Group Address: ``listId@this.server``

The ``smtp2gs`` script [#smtp2gs]_ detects when a VERP message arrives,
extracts the two addresses, and passes them to a form provided by this
product to `register a bounce`_.

Register a Bounce
=================

This product provides a form to register a bounce:
``/gs-group-member-bounce.html``. The form has three entries:

#. User Address,
#. Group Address, and
#. Token [#token]_.

When submitted, the form registers a **bounce** by making an entry in the
``bounce`` table. If the system has registered more than 5 bounces in the
last 60 days [#rate]_ then the email address is **unverified,** so no more
email will be sent to it. The form will send a notification to the member
if he or she has more than one email address.

* A ``bounce`` notification will be sent if the system has simply
  registered a bounce.

* A ``disabled`` notification will be sent if the email address has become
  unverified.

Pages
=====

This product provides two pages: 

* ``bounce.html`` in the group context lists the bounces that
  occur in the group.
* ``bounce.html`` in the profile context lists the bounces
  associated with a person.

The latter has not been linked, because currently (2014-07-31)
the Profile page is a mess, and it needs to be refactored.

Resources
=========

- Code repository: https://source.iopen.net/groupserver/gs.group.member.bounce
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

.. [#email] See ``gs.email`` for `an example 
            <http://source.iopen.net/groupserver/gs.email>`_
.. [#smtp2gs] See
   <http://source.iopen.net/groupserver/gs.group.messages.add.smtp2gs>
.. [#token] See <http://source.iopen.net/groupserver/gs.auth.token>
.. [#rate] An email address is not disabled immediately on a bounce because
           transient errors are common. The current hard-coded rate of 5
           bounces in 60 days has been informed by the wisdom of bitter
           experience.

..  LocalWords:  VERP smtp http groupserver
