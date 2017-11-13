from django.db import models
from fe_core.base_models import UUIDModel


class Arquivo(UUIDModel):
    arquivo = models.FileField()

    def __str__(self):
        return self.arquivo.name
