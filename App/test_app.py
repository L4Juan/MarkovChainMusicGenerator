import MarkovChain
import App
import unittest

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = App.MarkovChainGUI()
 
    def test_train(self):
        self.app._train()
        
if __name__ == "__main__":
    unittest.main()