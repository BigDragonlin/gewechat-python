import unittest
from unittest.mock import Mock
from unittest.mock import patch
from unittest.mock import MagicMock


def foo():
    return "Hello World"

class MockTestCase(unittest.TestCase):
    def testMock(self):
        mock = Mock()
        mock.return_value = "Hello World"
        print(mock())

    def testPatch(self):
        with patch(f"{self.__module__}.foo") as mock_foo: # Use self.__module__.foo as patch target
            mock_foo.return_value = "Hello"
            print(foo())

        with patch(f"{self.__module__}.foo") as mock_foo_inside: # Use different variable name for clarity
            mock_foo_inside.return_value = "Hello Inside"
            print(foo())

        print(foo())
    
    @patch(f"{__name__}.foo")
    def testPatchWithDecorator(self, mock_foo):
        mock_foo.return_value = "Hello"
        print(foo())