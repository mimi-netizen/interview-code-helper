import unittest
from src.app import create_app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome', response.data)

    def test_api(self):
        response = self.client.get('/api/some_endpoint')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Some response', response.data)

if __name__ == '__main__':
    unittest.main()