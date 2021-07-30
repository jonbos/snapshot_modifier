import unittest

from bs4 import BeautifulSoup as bs

from src.mapping import ResolutionMapping, GroupMapping, UserMapping

XML_STRING = '''
<stuff>
    <users nativeId="sansay" name="sansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>
    <groups nativeId="NOC" name="NOC"/>
    <resolutions nativeId="6" name="Completed" description=""/>
</stuff>

'''


class MyTestCase(unittest.TestCase):

    def test_update_resolution(self):
        soup = bs(XML_STRING, 'xml')
        row = {"old_name": "Completed", "new_name": "Complete"}
        expected = '''
        <stuff>
            <users nativeId="sansay" name="sansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>
            <groups nativeId="NOC" name="NOC"/>
            <resolutions nativeId="6" name="Complete" description=""/>
        </stuff>
        '''
        mapper = ResolutionMapping(row)
        mapper.apply(soup)
        self.assertEqual(soup, bs(expected, 'xml'))

    def test_update_group(self):
        soup = bs(XML_STRING, 'xml')
        row = {"old_name": "NOC", "new_name": "noc"}
        expected = '''
               <stuff>
                   <users nativeId="sansay" name="sansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>
                   <groups nativeId="noc" name="noc"/>
                   <resolutions nativeId="6" name="Completed" description=""/>
               </stuff>
               '''
        mapper = GroupMapping(row)
        mapper.apply(soup)
        self.assertEqual(soup, bs(expected, 'xml'))

    def test_update_user(self):
        soup = bs(XML_STRING, 'xml')
        row = {"old_name": "sansay", "new_name": "Serge.Ansay"}
        expected = '''
                      <stuff>
                          <users nativeId="Serge.Ansay" name="Serge.Ansay" fullName="Serge Ansay" email="Serge.Ansay@sony.com"/>
                          <groups nativeId="NOC" name="NOC"/>
                          <resolutions nativeId="6" name="Completed" description=""/>
                      </stuff>
                      '''
        mapper = UserMapping(row)
        mapper.apply(soup)
        self.assertEqual(soup, bs(expected, 'xml'))


if __name__ == '__main__':
    unittest.main()
