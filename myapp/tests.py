import json
from django.test import TestCase, Client


class MyappTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_ping_view(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.content), {"message": "pong"})

    # Add more tests for other views...
