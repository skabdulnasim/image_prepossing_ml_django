from django.urls import path
from .views import UploadImage, SaveCrop, PrescriptionImageList, CropLabelList

urlpatterns = [
    path('upload/', UploadImage.as_view(), name='upload'),
    path('save_crop/', SaveCrop.as_view(), name='save_crop'),
    path('originals/', PrescriptionImageList.as_view(), name='originals'),
    path('crops/', CropLabelList.as_view(), name='crops'),
]
