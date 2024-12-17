from django.db import models

class Domain(models.Model):
    id = models.AutoField(primary_key=True)
    domain_name = models.TextField()
    registrar_name = models.TextField()
    expiry_date = models.TextField()


    class Meta:
        db_table = 'domains'

    def __str__(self):
        return self.domain_name