import unittest
import objectid

class TestCreateObjectID(unittest.TestCase):
    """测试ObjectID
    """
    def test_single_process_create_objectid(self):
        id=objectid.create_objectid()
        print(id)
        
    
    
if __name__ == '__main__':
    unittest.main()