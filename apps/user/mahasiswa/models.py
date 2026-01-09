from django.db import models
from apps.accounts.models import User

class Mahasiswa(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'mahasiswa'},
        null=True, blank=True
    )
    name = models.TextField(max_length=200, null=True, blank=True)
    nim = models.CharField(max_length=20, unique=True)
    program_studi = models.CharField(max_length=100)
    angkatan = models.IntegerField()

    def __str__(self):
        return self.name or self.user.username