from datetime import datetime
from django.db import models

# Create your models here.
class Endpoint(models.Model):
    name = models.CharField(max_length=50,null=True)
    count = models.IntegerField(null=True)
    last_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['last_updated']
        verbose_name = "Endpoint"
        verbose_name_plural = "Endpoints"

    def __str__(self) -> str:
        return self.name.title()

class Resource(models.Model):
    name = models.CharField(max_length=100,null=True)
    index = models.IntegerField(null=True)
    last_updated = models.DateTimeField(default=datetime(2000,1,1,0,0,0,0))
    endpoint = models.ForeignKey(Endpoint,on_delete=models.CASCADE,null=True)
    data = models.JSONField(null=True)
    image = models.ImageField(upload_to='',null=True)

    class Meta:
        ordering = ['index']
        verbose_name = "Resource"
        verbose_name_plural = "Resources"
    
    def __str__(self) -> str:
        return str(self.endpoint)+" : "+self.name.title()
