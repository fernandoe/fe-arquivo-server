import mock
from django.core.urlresolvers import reverse
from django.test import TestCase

from arquivo.tests.factories import ArquivoFactory


class TestArquivoAPIView(TestCase):
    def __get_arquivo_url(self, uuid='00000000-0000-0000-0000-000000000000'):
        return reverse('arquivo', kwargs={'uuid': uuid})

    def test_get_status_code_404(self):
        response = self.client.get(self.__get_arquivo_url())
        self.assertEqual(404, response.status_code)

    def test_get_status_code_405(self):
        methods = ['post', 'put', 'delete', 'patch']
        for m in methods:
            response = getattr(self.client, m)(self.__get_arquivo_url())
            self.assertEqual(405, response.status_code)

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_get_status_code_200(self, mock_fieldfile_save):
        arquivo = ArquivoFactory()
        response = self.client.get(self.__get_arquivo_url(arquivo.uuid))
        self.assertEqual(200, response.status_code)
        mock_fieldfile_save.assert_called_once()

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_get_success_result_keys(self, mock_fieldfile_save):
        arquivo = ArquivoFactory()
        response = self.client.get(self.__get_arquivo_url(arquivo.uuid))
        self.assertCountEqual(response.data.keys(), ['uuid', 'created_at', 'updated_at', 'arquivo'])
        mock_fieldfile_save.assert_called_once()

    def test_get_success_invalid_uuid(self):
        response = self.client.get(self.__get_arquivo_url('invalid'))
        self.assertEqual(404, response.status_code)
