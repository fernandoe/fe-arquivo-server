import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase


class TestArquivoUploadAPIView(TestCase):
    def setUp(self):
        filename = "file.txt"
        content = b"file_content"
        self.file = SimpleUploadedFile(filename, content, content_type='multipart/form-data')

    @mock.patch("arquivo.views.default_storage")
    def test_post_201(self, mock_storage):
        response = self.client.post('/api/v1/arquivo', {'file': self.file}, format='multipart')
        self.assertEqual(201, response.status_code)
        mock_storage.save.assert_called_once()

    def test_post_400_file_not_send(self):
        response = self.client.post('/api/v1/arquivo', format='multipart')
        self.assertEqual(400, response.status_code)
