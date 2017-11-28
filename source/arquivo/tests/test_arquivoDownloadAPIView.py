import mock
from django.core.urlresolvers import reverse
from django.test import TestCase

from arquivo.tests.factories import ArquivoFactory


class TestArquivoDownloadAPIView(TestCase):
    def setUp(self):
        self.arquivo = None

    def tearDown(self):
        if self.arquivo is not None:
            self.arquivo.arquivo.delete()
            self.arquivo.delete()

    def __get_arquivo_url(self, uuid='00000000-0000-0000-0000-000000000000'):
        return reverse('arquivo_download', kwargs={'uuid': uuid})

    def test_get_status_code_200(self):
        self.arquivo = ArquivoFactory()
        response = self.client.get(self.__get_arquivo_url(self.arquivo.uuid))
        self.assertEqual(200, response.status_code)

    def test_get_status_code_405(self):
        methods = ['post', 'put', 'delete', 'patch']
        for m in methods:
            response = getattr(self.client, m)(self.__get_arquivo_url())
            self.assertEqual(405, response.status_code)

    def test_get_status_code_404(self):
        response = self.client.get(self.__get_arquivo_url())
        self.assertEqual(404, response.status_code)

    def test_get_success_invalid_uuid(self):
        response = self.client.get(self.__get_arquivo_url('invalid'))
        self.assertEqual(404, response.status_code)

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_get_404_file_not_exist_on_disk(self, mock_fieldfile_save):
        arquivo = ArquivoFactory(arquivo__filename='test_get_404_file_not_exist_on_disk.txt')
        response = self.client.get(self.__get_arquivo_url(arquivo.uuid))
        self.assertEqual(404, response.status_code)
        mock_fieldfile_save.assert_called_once()

    def test_get_success_content_disposition(self):
        self.arquivo = ArquivoFactory(arquivo__filename='test_get_success_invalid_uuid.txt')
        response = self.client.get(self.__get_arquivo_url(self.arquivo.uuid))
        self.assertEqual('attachment; filename=test_get_success_invalid_uuid.txt', response.get('Content-Disposition'))

    def test_get_success_content_length(self):
        self.arquivo = ArquivoFactory(arquivo__data='abc')
        response = self.client.get(self.__get_arquivo_url(self.arquivo.uuid))
        self.assertEqual('3', response.get('Content-Length'))

    def test_get_success_content(self):
        self.arquivo = ArquivoFactory(arquivo__data='abcdef')
        response = self.client.get(self.__get_arquivo_url(self.arquivo.uuid))
        self.assertEqual(b'abcdef', response.getvalue())
