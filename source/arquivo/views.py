import os
from django.core.exceptions import ValidationError
from django.http import Http404, FileResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from arquivo.models import Arquivo
from arquivo.serializers import ArquivoSerializer


class ArquivoUploadAPIView(APIView):
    def post(self, request, format=None):
        serializer = ArquivoSerializer(data=request.FILES)
        data = {}
        if serializer.is_valid():
            status_code = 201
            serializer.save()
            data = serializer.data
        else:
            status_code = 400
            data['errors'] = serializer.errors
        return Response(data=data, status=status_code)


class ArquivoAPIView(APIView):
    def get(self, request, uuid, format=None):
        try:
            arquivo = get_object_or_404(Arquivo, pk=uuid)
        except ValidationError:
            raise Http404
        serializer = ArquivoSerializer(arquivo)
        return Response(data=serializer.data, status=200)


class ArquivoDownloadAPIView(APIView):
    def get(self, request, uuid, format=None):
        try:
            arquivo = get_object_or_404(Arquivo, pk=uuid)
        except ValidationError:
            raise Http404
        file_path = arquivo.arquivo.path
        if os.path.exists(file_path):
            response = FileResponse(open(file_path, 'rb'))
            response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
            response['Content-Length'] = os.path.getsize(file_path)
            return response
        raise Http404
