from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from .models import PrescriptionImage, CropLabel
from .serializers import PrescriptionImageSerializer, CropLabelSerializer
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw
import base64, io, os, math
from django.conf import settings

class UploadImage(APIView):
    def post(self, request, format=None):
        file = request.FILES.get('image')
        if not file:
            return Response({'detail': 'No image uploaded'}, status=status.HTTP_400_BAD_REQUEST)
        p = PrescriptionImage.objects.create(image=file)
        return Response({'id': p.id, 'url': p.image.url}, status=status.HTTP_201_CREATED)

class SaveCrop(APIView):
    """
    Expected JSON payload:
    {
    "original_id": 4,
    "label": "Combiflam",
    "gender": "M",
    "age": "45",
    "bbox": { "x": 120, "y": 260, "width": 300, "height": 120 },
    "rotate": 12,
    "zoom": 1.8,
    "pan": { "x": -50, "y": 30 }
    }
    Coordinates must be in original image pixel coordinates.
    """
    def post(self, request, format=None):
        data = request.data

        try:
            original = PrescriptionImage.objects.get(id=data['original_id'])
        except:
            return Response({'detail': 'original not found'}, status=400)

        im = Image.open(original.image.path).convert("RGB")

        # ✅ NEW: incoming transform params
        rotate = float(data.get("rotate", 0))      # degrees
        zoom = float(data.get("zoom", 1))          # 1.0 = no zoom
        pan = data.get("pan", {"x": 0, "y": 0})

        # ✅ APPLY ZOOM (resize)
        if zoom != 1:
            w = int(im.width * zoom)
            h = int(im.height * zoom)
            im = im.resize((w, h), Image.LANCZOS)

        # ✅ APPLY ROTATION (around center)
        if rotate != 0:
            im = im.rotate(rotate, expand=True)

        # ✅ APPLY PAN (move the canvas)
        if pan and (pan.get("x") or pan.get("y")):
            new_canvas = Image.new("RGB", (im.width, im.height), (255, 255, 255))
            new_canvas.paste(im, (int(pan["x"]), int(pan["y"])))
            im = new_canvas

        # ✅ CROP
        if data.get("bbox"):
            b = data["bbox"]
            x, y = int(b["x"]), int(b["y"])
            w, h = int(b["width"]), int(b["height"])
            cropped = im.crop((x, y, x + w, y + h))
        else:
            return Response({"detail": "bbox not provided"}, status=400)

        # ✅ Save cropped file
        output = io.BytesIO()
        cropped.save(output, format="JPEG", quality=90)
        output.seek(0)

        filename = f"crop_{original.id}_{CropLabel.objects.count()}.jpg"
        cropped_file = ContentFile(output.read(), name=filename)

        saved = CropLabel.objects.create(
            original=original,
            cropped_image=cropped_file,
            label=data.get("label", ""),
            gender=data.get("gender", ""),
            age=data.get("age", ""),
            bbox=data.get("bbox"),
            # ✅ store params for reproducibility
            rotate=rotate,
            zoom=zoom,
            pan=pan
        )

        return Response(CropLabelSerializer(saved).data, status=201)
    
# Optional helpers to list originals and crops
class PrescriptionImageList(generics.ListAPIView):
    queryset = PrescriptionImage.objects.all().order_by('-uploaded_at')
    serializer_class = PrescriptionImageSerializer

class CropLabelList(generics.ListAPIView):
    queryset = CropLabel.objects.all().order_by('-created_at')
    serializer_class = CropLabelSerializer
