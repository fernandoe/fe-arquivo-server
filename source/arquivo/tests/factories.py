import factory

from .. import models


class ArquivoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Arquivo

    arquivo = factory.django.FileField()
