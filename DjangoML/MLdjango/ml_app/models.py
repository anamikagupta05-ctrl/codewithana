from django.db import models

# Create your models here.


class PredictionModel(models.Model):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    # Files will be stored in MEDIA_ROOT/uploads/
    file = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return f"Prediction {self.id} - {self.title}"