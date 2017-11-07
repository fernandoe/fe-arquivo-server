from django.core.files.storage import default_storage
from rest_framework.response import Response
from rest_framework.views import APIView


class ArquivoUploadAPIView(APIView):
    def post(self, request, format=None):
        arquivo = request.FILES.get('file', None)
        if arquivo is not None:
            default_storage.save(None, arquivo)
            status_code = 201
        else:
            status_code = 400
        return Response(status=status_code)
