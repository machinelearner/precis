from unittest import TestCase
import os.path as ospath
from precis.core import Document
from precis.utils import FileReader


class FileReaderTest(TestCase):
    def setUp(self):
        self.path = ospath.join(ospath.dirname(__file__), "test_data/inception/Inception - 2")

    def test_shouldReadFromFile(self):
        expected_file_content = """This is content of the file.\nWith line separated. blabla"""
        expected_document = Document(text=expected_file_content)

        actual_document = Document(text=FileReader.read(self.path))

        self.assertEquals(actual_document,expected_document)