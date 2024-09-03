import unittest

from modules.env import Env
from modules.ai import AI

class Tests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.text_example = 'Croatian mountians'
        
    def setUp(self):
        pass
        
    def test_1(self):
        creating_env_response = Env.create()
        self.assertTrue(creating_env_response)
        
    async def test_2(self):
        with AI() as ai_class:
            generate_image_response = await ai_class.generate_image(self.text_example)
        
        status = generate_image_response['status']
        self.assertTrue(status)
        
    def tearDown(self):
        pass
        
    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
