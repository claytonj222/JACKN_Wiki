import unittest
from JACKN_Wiki.ActiveUsersAPI.ActiveUsers import findActiveUsers


class TestActiveUsers(unittest.TestCase):

    def test_findActiveUsers(self):
        users = {
                  "name": {
                    "active": True,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                  },
                  "sam": {
                    "active": True,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                  }
                }
        list = findActiveUsers(users)
        print(list)
        testlist = ['name', 'sam']
        self.assertEqual(list, testlist)

    def test_findActiveUsers_someFalse(self):
        users = {
                "name": {
                    "active": True,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                },
                "sam": {
                    "active": False,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                },
                "vu": {
                    "active": True,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                }
            }
        list = findActiveUsers(users)
        print(list)
        testlist = ['name', 'vu']
        self.assertEqual(list, testlist)

    def test_findActiveUsers_allFalse(self):
        users = {
                "name": {
                    "active": False,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                },
                "sam": {
                    "active": False,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                },
                "vu": {
                    "active": False,
                    "authentication_method": "cleartext",
                    "password": "1234",
                    "authenticated": True,
                    "roles": []
                }
            }
        list = findActiveUsers(users)
        print(list)
        testlist = []
        self.assertEqual(list, testlist)

if __name__ == '__main__':
    unittest.main()
