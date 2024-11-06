from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class ProvidersViewSet(ViewSet):

    def list(self, request):
        content = {"providers": ["gemini", "openai", "llama"]}
        return Response(content, status.HTTP_200_OK)
