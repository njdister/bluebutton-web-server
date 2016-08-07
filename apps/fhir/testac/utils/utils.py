#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

"""
hhs_oauth_server
FILE: utils
Created: 7/25/16 4:21 PM

File created by: ''
"""
from apps.fhir.bluebutton.models import Crosswalk


def get_posted_resource_id(outcome, status_code):
    """ Look at result from a POST to get Resource ID
    {'issue': [{'severity': 'information',
            'code': 'informational',
            'diagnostics': 'Successfully created resource "Patient/9334211/_history/1" in 47ms'}],
            'resourceType': 'OperationOutcome'}

    outcome is json
    """

    # print("\nOutcome:%s" % outcome)
    issue = outcome
    if status_code == 201:
        # We have a successful write
        # print("\nIssue:%s" % issue)
        if 'diagnostics' not in issue['issue'][0]:
            return

        # print("\nIssue-diags:%s" % issue['issue'][0])
        diagnostics = issue['issue'][0]['diagnostics']

        # Now we split out the text to find the Patient/Id

        pieces = diagnostics.split('"')
        resource_id = pieces[1].split('/_')
        id = resource_id[0]
        # print("Pieces: %s" % pieces)
        # print("ID:%s" % id)

        return id
    # print("\nStatus_code:%s" % status_code)

    return


def update_crosswalk(request, id):
    """ Look up Crosswalk for user and add patient_id """

    try:
        xwalk = Crosswalk.objects.get(user=request.user)
    except Crosswalk.DoesNotExist:
        xwalk = Crosswalk()
        xwalk.user = request.user

    if xwalk.fhir_id:
        return xwalk
    else:
        xwalk.fhir_id = id
        xwalk.save()

    return xwalk


def get_bb_claims(json_stuff):
    """ Get Claims from BB Json """

    if not json_stuff:
        return

    if 'claims' in json_stuff:
        return json_stuff['claims']
    else:
        return
