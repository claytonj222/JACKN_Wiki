import os
import unittest
from RandomPageRedirect.RandPageRedirect import seedRNG, determineValueForRedirect, determinePageForRedirect
from Wiki440.wiki.web import create_app, current_wiki


class TestRandPageRedirect(unittest.TestCase):

    def setUp(self):

        app = create_app(os.getcwd())

        app.config['TESTING'] = True
        with app.test_request_context():
            self.pages = current_wiki.index()


    def test_seedGeneration(self):
        seedRNG(1)
        value = determineValueForRedirect(self.pages)
        seedRNG(256000)
        value2 = determineValueForRedirect(self.pages)
        self.assertEqual(value, 3)
        self.assertEqual(value2, 5)


    def test_pageChoice(self):
        seedRNG(20)
        value = determineValueForRedirect(self.pages)
        page = determinePageForRedirect(self.pages, value)
        self.assertEqual(value, 11)
        self.assertEqual(page, "test9")



if __name__ == '__main__':
    unittest.main()