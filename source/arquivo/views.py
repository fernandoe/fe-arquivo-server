from rest_framework.response import Response
from rest_framework.views import APIView

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
