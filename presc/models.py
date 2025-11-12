from django.db import models

class PrescriptionImage(models.Model):
    image = models.ImageField(upload_to='originals/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'PrescriptionImage {self.id}'

class CropLabel(models.Model):
    original = models.ForeignKey(PrescriptionImage, related_name='crops', on_delete=models.CASCADE)
    cropped_image = models.ImageField(upload_to='crops/')
    label = models.CharField(max_length=255)
    gender = models.CharField(max_length=20, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    # store selection metadata for reproducibility
    bbox = models.JSONField(blank=True, null=True)       # {x,y,width,height}
    polygon = models.JSONField(blank=True, null=True)    # [[x,y], [x,y], ...]
    rotate = models.FloatField(default=0)
    zoom = models.FloatField(default=1)
    pan = models.JSONField(blank=True, null=True)   # {"x":number,"y":number}
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'CropLabel {self.id} ({self.label})'
