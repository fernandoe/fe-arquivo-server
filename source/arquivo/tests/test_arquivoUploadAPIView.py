import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings


class TestArquivoUploadAPIView(TestCase):
    def setUp(self):
        filename = "file.txt"
        content = b"file_content"
        self.file = SimpleUploadedFile(filename, content, content_type='multipart/form-data')

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_post_201(self, mock_fieldfile_save):
        response = self.client.post('/api/v1/arquivo', {'arquivo': self.file}, format='multipart')
        self.assertEqual(201, response.status_code)
        mock_fieldfile_save.assert_called_once()

    def test_post_400_file_not_send(self):
        response = self.client.post('/api/v1/arquivo', format='multipart')
        self.assertEqual(400, response.status_code)

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_post_success_keys(self, mock_fieldfile_save):
        response = self.client.post('/api/v1/arquivo', {'arquivo': self.file}, format='multipart')
        mock_fieldfile_save.assert_called_once()
        self.assertCountEqual(response.data.keys(), ['uuid', 'created_at', 'updated_at', 'arquivo'])

    def test_post_errors_keys(self):
        response = self.client.post('/api/v1/arquivo', format='multipart')
        self.assertCountEqual(response.data.keys(), ['errors'])

    def test_post_error_field_arquivo_not_sent(self):
        response = self.client.post('/api/v1/arquivo', format='multipart')
        self.assertTrue('errors' in response.data)
        self.assertTrue('arquivo' in response.data['errors'])
        self.assertTrue(1, len(response.data['errors']['arquivo']))
        self.assertEqual('No file was submitted.', response.data['errors']['arquivo'][0])

    @override_settings(LANGUAGE_CODE='pt-br')
    def test_post_error_field_arquivo_not_sent_in_br(self):
        response = self.client.post('/api/v1/arquivo', format='multipart')
        self.assertTrue('errors' in response.data)
        self.assertTrue('arquivo' in response.data['errors'])
        self.assertTrue(1, len(response.data['errors']['arquivo']))
        self.assertEqual('Nenhum arquivo foi submetido.', response.data['errors']['arquivo'][0])