from django.db import models

# Create your models here.

class UploadPDF(models.Model):
    name = models.FileField(upload_to='pdf/')
    uploadDate = models.DateTimeField(auto_now_add=True, auto_now=False,verbose_name='Date')

    def __str__(self):
        return self.name