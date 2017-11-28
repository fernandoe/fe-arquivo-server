import mock
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from arquivo.serializers import ArquivoSerializer
from arquivo.tests.factories import ArquivoFactory


class TestArquivoSerializer(TestCase):

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def setUp(self, mock_fieldfile_save):
        self.data = {
            'arquivo': SimpleUploadedFile('data.txt', 'content data'.encode())
        }
        self.arquivo = ArquivoFactory()
        self.serializer = ArquivoSerializer(instance=self.arquivo)

    def test_contains_expected_fields(self):
        data = self.serializer.data
        self.assertCountEqual(data.keys(), ['uuid', 'created_at', 'updated_at', 'arquivo'])

    def test_field_uuid(self):
        data = self.serializer.data
        self.assertEqual(data['uuid'], str(self.arquivo.uuid))

    def test_field_arquivo(self):
        data = self.serializer.data
        self.assertEqual(data['arquivo'], self.arquivo.arquivo)

    def test_is_valid(self):
        serializer = ArquivoSerializer(data=self.data)
        self.assertTrue(serializer.is_valid())

    def test_is_not_valid_arquivo_nao_informado(self):
        serializer = ArquivoSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertCountEqual(serializer.errors, ['arquivo'])
