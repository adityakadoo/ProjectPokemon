from django.db import models

# Create your models here.
class Cluster(models.Model):
    name = models.CharField(max_length=30,null=True)
    size = models.IntegerField(null=True)
    elements = models.JSONField(null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "Cluster"
        verbose_name_plural = "Clusters"
    
    def __str__(self) -> str:
        return self.name.title() + "(" + str(self.size) + ")"