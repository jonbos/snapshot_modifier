import unittest

from src.mapping_functions import GroupMappingFunction


class GroupMappingTest(unittest.TestCase):
    def test_modifies_group(self):
        pass

class UserMappingTest(unittest.TestCase):
    def test_modifies_user(self):
        replacement_dict = {"old_name": "sansay", "new_name": "Serge.Ansay"}
        row = '<users nativeId="sansay" name="sansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>'
        expected = '<users nativeId="Serge.Ansay" name="Serge.Ansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>'
        actual = GroupMappingFunction(replacement_dict).apply(row)
        self.assertEqual(expected, actual)

class ResolutionMappingTest(unittest.TestCase):
    def test_modified_user(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
