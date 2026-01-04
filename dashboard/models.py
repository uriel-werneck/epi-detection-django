from django.db import models
from django.utils import timezone

# Create your models here.
class Detection(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='detections')
    file_name = models.CharField(max_length=200, null=False, blank=False)
    detection_data = models.TextField(null=False, blank=False)
    timestamp = models.DateTimeField(default=timezone.now)
    upload_type = models.CharField(max_length=20, null=False, blank=False)   # Alterado para suportar 'upload-video'
    quantity = models.IntegerField(null=False, blank=False)
    detected_classes = models.TextField(null=False, blank=False)
    # Novos campos para armazenar imagens e vídeos no banco de dados
    image_data = models.ImageField(upload_to='detections/images/', null=True, blank=True)
    video_data = models.FileField(upload_to='detections/videos/', null=True, blank=True)
    is_stored_in_db = models.BooleanField(default=False) # Indica se está armazenado no banco

    class Meta:
        db_table = 'detections'

    def __str__(self):
        return f'Detection {self.id} - User {self.user.id}'