import logging

import mock
from django.db import DatabaseError
from django.test import TestCase
from rest_framework.test import APIClient


class TestHealthCheckAPIView(TestCase):
    cursor_wrapper = mock.Mock()
    cursor_wrapper.side_effect = DatabaseError

    def setUp(self):
        self.client = APIClient()
        logging.disable(logging.CRITICAL)

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_get_200(self):
        response = self.client.get('/healthcheck')
        self.assertEqual(200, response.status_code)

    def test_get_database(self):
        response = self.client.get('/healthcheck')
        self.assertTrue(response.data['database'])

    @mock.patch("healthcheck.views.connection.cursor", cursor_wrapper)
    def test_get_database_error(self):
        response = self.client.get('/healthcheck')
        self.assertFalse(response.data['database'])
