from oauth2_provider.compat import parse_qs, urlparse
from oauth2_provider.models import get_access_token_model
from django.core.urlresolvers import reverse
from django.test import Client

from apps.test import BaseApiTest
from ..models import Application

AccessToken = get_access_token_model()


class TestAuthorizeWithCustomScheme(BaseApiTest):
    def test_post_with_valid_non_standard_scheme(self):
        redirect_uri = 'com.custom.bluebutton://example.it'
        # create a user
        self._create_user('anna', '123456')
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app',
            grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris=redirect_uri)
        application.scope.add(capability_a, capability_b)

        # user logs in
        self.client.login(username='anna', password='123456')

        code_challenge = "sZrievZsrYqxdnu2NVD603EiYBM18CuzZpwB-pOSZjo"

        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        }
        response = self.client.get('/v1/o/authorize', data=payload)
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
            'code_challenge': code_challenge,
            'code_challenge_method': 'S256',
        }
        response = self.client.post(response['Location'], data=payload)

        self.assertEqual(response.status_code, 302)
        # now extract the authorization code and use it to request an access_token
        query_dict = parse_qs(urlparse(response['Location']).query)
        authorization_code = query_dict.pop('code')
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'code_verifier': 'test123456789123456789123456789123456789123456789',
        }
        response = self.client.post(reverse('oauth2_provider:token'), data=token_request_data)
        self.assertEqual(response.status_code, 200)

    def test_post_with_invalid_non_standard_scheme(self):
        redirect_uri = 'com.custom.bluebutton://example.it'
        bad_redirect_uri = 'com.custom.bad://example.it'
        # create a user
        self._create_user('anna', '123456')
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app',
            grant_type=Application.GRANT_AUTHORIZATION_CODE,
            redirect_uris=redirect_uri)
        application.scope.add(capability_a, capability_b)
        # user logs in
        self.client.login(username='anna', password='123456')
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': bad_redirect_uri,
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
        }
        response = self.client.post(reverse('oauth2_provider:authorize'), data=payload)

        self.assertEqual(response.status_code, 400)

    def test_refresh_token(self):
        redirect_uri = 'http://localhost'
        # create a user
        self._create_user('anna', '123456')
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app',
            grant_type=Application.GRANT_AUTHORIZATION_CODE,
            client_type=Application.CLIENT_CONFIDENTIAL,
            redirect_uris=redirect_uri)
        application.scope.add(capability_a, capability_b)
        # user logs in
        self.client.login(username='anna', password='123456')
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
        }
        response = self.client.post(reverse('oauth2_provider:authorize'), data=payload)
        self.client.logout()
        self.assertEqual(response.status_code, 302)
        # now extract the authorization code and use it to request an access_token
        query_dict = parse_qs(urlparse(response['Location']).query)
        authorization_code = query_dict.pop('code')
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        c = Client()
        response = c.post('/v1/o/token/', data=token_request_data)
        self.assertEqual(response.status_code, 200)
        # Now we have a token and refresh token
        tkn = response.json()['access_token']
        refresh_tkn = response.json()['refresh_token']
        refresh_request_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_tkn,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        response = self.client.post(reverse('oauth2_provider:token'), data=refresh_request_data)
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.json()['access_token'], tkn)

    def test_refresh_with_expired_token(self):
        redirect_uri = 'http://localhost'
        # create a user
        self._create_user('anna', '123456')
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app',
            grant_type=Application.GRANT_AUTHORIZATION_CODE,
            client_type=Application.CLIENT_CONFIDENTIAL,
            redirect_uris=redirect_uri)
        application.scope.add(capability_a, capability_b)
        # user logs in
        self.client.login(username='anna', password='123456')
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
        }
        response = self.client.post(reverse('oauth2_provider:authorize'), data=payload)
        self.client.logout()
        self.assertEqual(response.status_code, 302)
        # now extract the authorization code and use it to request an access_token
        query_dict = parse_qs(urlparse(response['Location']).query)
        authorization_code = query_dict.pop('code')
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        c = Client()
        response = c.post('/v1/o/token/', data=token_request_data)
        self.assertEqual(response.status_code, 200)
        # Now we have a token and refresh token
        tkn = response.json()['access_token']
        refresh_tkn = response.json()['refresh_token']
        at = AccessToken.objects.get(token=tkn)
        at.delete()
        refresh_request_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_tkn,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        response = self.client.post(reverse('oauth2_provider:token'), data=refresh_request_data)
        self.assertEqual(response.status_code, 404)

    def test_refresh_with_revoked_token(self):
        redirect_uri = 'http://localhost'
        # create a user
        self._create_user('anna', '123456')
        capability_a = self._create_capability('Capability A', [])
        capability_b = self._create_capability('Capability B', [])
        # create an application and add capabilities
        application = self._create_application(
            'an app',
            grant_type=Application.GRANT_AUTHORIZATION_CODE,
            client_type=Application.CLIENT_CONFIDENTIAL,
            redirect_uris=redirect_uri)
        application.scope.add(capability_a, capability_b)
        # user logs in
        self.client.login(username='anna', password='123456')
        # post the authorization form with only one scope selected
        payload = {
            'client_id': application.client_id,
            'response_type': 'code',
            'redirect_uri': redirect_uri,
            'scope': ['capability-a'],
            'expires_in': 86400,
            'allow': True,
        }
        response = self.client.post(reverse('oauth2_provider:authorize'), data=payload)
        self.client.logout()
        self.assertEqual(response.status_code, 302)
        # now extract the authorization code and use it to request an access_token
        query_dict = parse_qs(urlparse(response['Location']).query)
        authorization_code = query_dict.pop('code')
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        c = Client()
        response = c.post('/v1/o/token/', data=token_request_data)
        self.assertEqual(response.status_code, 200)
        # Now we have a token and refresh token
        tkn = response.json()['access_token']
        revoke_request_data = {
            'token': tkn,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        rev_response = c.post('/v1/o/revoke_token/', data=revoke_request_data)
        self.assertEqual(rev_response.status_code, 200)
        refresh_tkn = response.json()['refresh_token']
        refresh_request_data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_tkn,
            'redirect_uri': redirect_uri,
            'client_id': application.client_id,
            'client_secret': application.client_secret,
        }
        response = self.client.post(reverse('oauth2_provider:token'), data=refresh_request_data)
        self.assertEqual(response.status_code, 404)