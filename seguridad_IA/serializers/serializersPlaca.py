# ia/serializers.py
from rest_framework import serializers
from ..models import LecturaPlaca

class AlprScanSerializer(serializers.Serializer):
    image_url = serializers.URLField(required=False)
    image_b64 = serializers.CharField(required=False, allow_blank=True)
    upload    = serializers.ImageField(required=False)   # <— NUEVO
    camera_id = serializers.CharField(required=False, allow_blank=True)
    regions   = serializers.CharField(required=False, allow_blank=True)  # ej: "bo"

    def validate(self, attrs):
        if not (attrs.get("image_url") or attrs.get("image_b64") or attrs.get("upload")):
            raise serializers.ValidationError("Debes enviar 'image_url', 'image_b64' o 'upload'.")
        return attrs

class LecturaPlacaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecturaPlaca
        fields = "__all__"
