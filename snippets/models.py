from django.db import models

class Snippet(models.Model):
    content = models.BinaryField()  
    encrypted = models.BooleanField(default=False)  

    def __str__(self):
        return f'Snippet {self.id}'
