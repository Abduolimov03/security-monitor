from django.db import models

class DomainRecord(models.Model):
    domain = models.CharField(max_length=255)
    email = models.EmailField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.domain} -> {self.email}"
