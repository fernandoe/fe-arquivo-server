import mock
from django.db import models
from django.test import TestCase

from arquivo.models import Arquivo
from arquivo.tests.factories import ArquivoFactory


class TestArquivo(TestCase):

    def test_field_uuid(self):
        field = Arquivo._meta.get_field('uuid')
        self.assertTrue(isinstance(field, models.UUIDField))
        self.assertTrue(field.primary_key)

    def test_field_created_at(self):
        field = Arquivo._meta.get_field('created_at')
        self.assertTrue(isinstance(field, models.DateTimeField))
        self.assertTrue(field.auto_now_add)
        self.assertFalse(field.auto_now)

    def test_field_updated_at(self):
        field = Arquivo._meta.get_field('updated_at')
        self.assertTrue(isinstance(field, models.DateTimeField))
        self.assertFalse(field.auto_now_add)
        self.assertTrue(field.auto_now)

    def test_field_arquivo(self):
        field = Arquivo._meta.get_field('arquivo')
        self.assertTrue(isinstance(field, models.FileField))

    @mock.patch("django.db.models.fields.files.FieldFile.save")
    def test_str(self, mock_storage):
        name = 'darth-vader.txt'
        arquivo = ArquivoFactory(arquivo__filename=name)
        self.assertEqual(name, str(arquivo))
        mock_storage.assert_called_once()
