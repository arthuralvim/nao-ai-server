from django.urls import reverse
from rest_framework import status as status_code


class TestProvidersBase:

    def test_should_return_available_providers(self, api_client):
        response = api_client.get(reverse("api:providers-list"))
        assert response.data["providers"] == ["gemini", "openai", "llama"]
        assert response.status_code == status_code.HTTP_200_OK
