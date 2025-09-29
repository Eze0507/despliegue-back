# vehiculo/views.py
import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers.serializersVehiculo import VehiculoSerializer, PersonaAuxSerializers
from .serializers.serializersBloque import BloqueSerializer
from .serializers.serializersUnidad import UnidadSerializer, BloqueAuxSerializer
from .serializers.serializersIncidente import IncidenteSerializer
from .modelsVehiculo import Vehiculo, Bloque, Unidad, incidente
from decouple import config
from .models import Persona
from django.conf import settings



class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def create(self, request, *args, **kwargs):
        return self.handle_image_upload(request, super().create)

    def update(self, request, *args, **kwargs):
        return self.handle_image_upload(request, super().update, *args, **kwargs)

    def handle_image_upload(self, request, action, *args, **kwargs):
        imagen_file = request.FILES.get("imagen")

        if imagen_file:
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": settings.IMGBB_API_KEY}
            files = {"image": imagen_file.read()}
            response = requests.post(url, payload, files=files)

            if response.status_code == 200:
                image_url = response.json()["data"]["url"]
                data = request.data.copy()
                data["imagen"] = image_url
                request._full_data = data
            else:
                return Response({"error": "Error al subir imagen a ImgBB"}, status=500)

        else:
            if request.method in ["PUT", "PATCH"]:
                instance = self.get_object()
                data = request.data.copy()
                if not data.get("imagen"):
                    data["imagen"] = instance.imagen
                    request._full_data = data

        return action(request, *args, **kwargs)
    
class personaAuxViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaAuxSerializers

class BloqueViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueSerializer

class UnidadViewSet(viewsets.ModelViewSet):
    queryset = Unidad.objects.all()
    serializer_class = UnidadSerializer

    def create(self, request, *args, **kwargs):
        return self.handle_image_upload(request, super().create)

    def update(self, request, *args, **kwargs):
        return self.handle_image_upload(request, super().update, *args, **kwargs)

    def handle_image_upload(self, request, action, *args, **kwargs):
        imagen_file = request.FILES.get("imagen")

        if imagen_file:
            url = "https://api.imgbb.com/1/upload"
            payload = {"key": settings.IMGBB_API_KEY}
            files = {"image": imagen_file.read()}
            response = requests.post(url, payload, files=files)

            if response.status_code == 200:
                image_url = response.json()["data"]["url"]
                data = request.data.copy()
                data["imagen"] = image_url
                request._full_data = data
            else:
                return Response({"error": "Error al subir imagen a ImgBB"}, status=500)

        else:
            if request.method in ["PUT", "PATCH"]:
                instance = self.get_object()
                data = request.data.copy()
                if not data.get("imagen"):
                    data["imagen"] = instance.imagen
                    request._full_data = data

        return action(request, *args, **kwargs)


class BloqueAuxViewSet(viewsets.ModelViewSet):
    queryset = Bloque.objects.all()
    serializer_class = BloqueAuxSerializer

class IncidenteViewSet(viewsets.ModelViewSet):
    queryset = incidente.objects.all()
    serializer_class = IncidenteSerializer
