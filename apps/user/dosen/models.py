from django.db import models
from apps.accounts.models import User

class Dosen(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'dosen'},
        null=True, blank=True
    )
    name = models.TextField(max_length=200, null=True, blank=True)
    nidn = models.TextField(max_length=20, unique=True)
    fakultas = models.CharField(max_length=100)

    def __str__(self):
        return self.name or self.user.username