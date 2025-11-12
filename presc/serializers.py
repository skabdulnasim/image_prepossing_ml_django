# presc/serializers.py
from rest_framework import serializers
from .models import PrescriptionImage, CropLabel

class PrescriptionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrescriptionImage
        fields = ['id', 'image', 'uploaded_at']

class CropLabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropLabel
        fields = [
            'id',
            'original',
            'cropped_image',
            'label',
            'gender',
            'age',
            'bbox',
            'polygon',
            'created_at'
        ]
