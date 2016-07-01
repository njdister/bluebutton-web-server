from django.test import TestCase, RequestFactory


class BlueButtonReadRequestTest(TestCase):

    def setUp(self):
        # Setup the RequestFactory
        self.factory = RequestFactory()
        self.fixtures = [
            'fhir_bluebutton_testdata_prep.json',
            'fhir_server_testdata_prep.json',
        ]

    def fhir_bluebutton_read_testcase(self):
        """
        Patient Not Allowed - No Crosswalk
        """
        # TODO: complete this test
        self.factory.get('/bluebutton/fhir/v1/Patient')


class ConformanceFilterTest(TestCase):
    """ Test that Conformance Statement is filtered """

    # TODO: Write a test using Patient as supported resource.

    # Setup Patient in Supported Resource

    # Make call to Conformance Statement

    # Test that Patient is only resource displayed
