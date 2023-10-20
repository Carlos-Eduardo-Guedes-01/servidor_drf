from rest_framework import viewsets
from .models import Modelo
from .serializers import ModeloSerializer
from rest_framework.response import Response
from rest_framework import status
import os
from django.conf import settings
from ultralytics import YOLO
from tempfile import NamedTemporaryFile
from PIL import Image
from rest_framework.views import APIView
from rest_framework import permissions


class Verification(viewsets.ModelViewSet):
    serializer_class = ModeloSerializer
    queryset = Modelo.objects.all()
    model=Modelo
    permission_classes = [permissions.AllowAny]
    def create(self, request):
        # Obtém o modelo anterior, se existir
        modelo_anterior = Modelo.objects.first()

        # Continua com a criação do novo modelo
        dado = request.FILES.get('modelo_v')
        c = Modelo(modelo_v=dado)
        c.save()

        # Exclui o modelo anterior, se existir
        if modelo_anterior:
            # Exclui o arquivo associado da pasta de mídia
            if modelo_anterior.modelo_v:
                path_to_file = os.path.join(settings.MEDIA_ROOT, str(modelo_anterior.modelo_v))
                if os.path.exists(path_to_file):
                    os.remove(path_to_file)
            
            modelo_anterior.delete()

        return Response("Carregado!", status=status.HTTP_201_CREATED)
        
class VideoStreamingView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        if 'frame' not in request.FILES:
            return Response({'error': 'Quadro não encontrado no formulário'}, status=400)

        frame = request.FILES['frame']
        CONFIDENCE_THRESHOLD = 0.35

        # Carregando o modelo treinado YOLO
        queryset = Modelo.objects.first()
        model_path = queryset.modelo_v.path
        model = YOLO(model_path)

        # Abrir o quadro usando PIL para garantir que seja uma imagem suportada
        with NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(frame.read())
        frame_path = temp_file.name
        image = Image.open(frame_path)

        # Executando o modelo YOLO para detecção de objetos no frame
        detections = model(image)[0]

        # Lista para armazenar as bounding boxes que a detecção retorna
        results = []

        # DETECÇÃO
        for data in detections.boxes.data.tolist():
            # Extrai a confiança associada à predição
            confidence = data[4]

            # Filtra detecções fracas
            if float(confidence) < CONFIDENCE_THRESHOLD:
                continue

            # Obtém coordenadas da bounding box e a classe
            xmin, ymin, xmax, ymax = int(data[0]), int(data[1]), int(data[2]), int(data[3])
            class_id = int(data[5])

            # Adiciona as informações à lista de resultados como um dicionário
            results.append({'xmin': xmin, 'ymin': ymin, 'width': xmax - xmin, 'height': ymax - ymin})

        # Retorna a lista de resultados como uma resposta JSON
        print(results)
        return Response(results)

    
    