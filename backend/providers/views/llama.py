import requests
from django.conf import settings
from providers.serializers import (
    PromptSerializer,
    ProviderResponseSerializer,
    build_prompt_llama,
)
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class LlamaViewSet(ViewSet):

    @action(detail=False, url_path="status", url_name="status")
    def status(self, request):
        try:
            r = requests.get(settings.LLAMA_ENDPOINT + "/api/tags")
            r.raise_for_status()
        except Exception:
            return Response({"status": "unavailable provider"}, status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response({"status": "running"}, status.HTTP_200_OK)

    @action(detail=False, url_path="models", url_name="models")
    def models(self, request):
        r = requests.get(settings.LLAMA_ENDPOINT + "/api/tags")
        r.raise_for_status()
        response = r.json()
        content = {"models": [model["name"] for model in response["models"]]}
        return Response(content, status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["POST"],
        url_path="prompt",
        url_name="prompt",
    )
    def prompt(self, request):
        data = JSONParser().parse(request)
        prompt = PromptSerializer(data=data)

        if prompt.is_valid():
            payload = build_prompt_llama(model=prompt.validated_data["model"], prompt=prompt.validated_data["prompt"])
            response = requests.post(settings.LLAMA_ENDPOINT + "/api/generate", json=payload)
            response.raise_for_status()
            response = response.json()
            provider_response = ProviderResponseSerializer(data={"provider": "llama", "response": response["response"]})
            assert provider_response.is_valid()
            return Response(provider_response.data, status.HTTP_200_OK)
        return Response(prompt.errors, status.HTTP_400_BAD_REQUEST)
