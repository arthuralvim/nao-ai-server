import pytest
from django.urls import reverse
from rest_framework import status as status_code


class TestProviderLlama:

    def test_should_return_correct_url(self):
        assert reverse("api:llama-status") == "/provider/llama/status/"
        assert reverse("api:llama-models") == "/provider/llama/models/"
        assert reverse("api:llama-prompt") == "/provider/llama/prompt/"

    @pytest.mark.default_cassette("llama_status_off.yaml")
    @pytest.mark.vcr
    def test_should_return_llama_status_off(self, api_client):
        response = api_client.get(reverse("api:llama-status"))
        assert response.status_code == status_code.HTTP_503_SERVICE_UNAVAILABLE

    @pytest.mark.default_cassette("llama_status_on.yaml")
    @pytest.mark.vcr
    def test_should_return_llama_status_on(self, api_client):
        response = api_client.get(reverse("api:llama-status"))
        assert response.data == {"status": "running"}
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("llama_models.yaml")
    @pytest.mark.vcr
    def test_should_return_llama_models(self, api_client):
        response = api_client.get(reverse("api:llama-models"))
        assert "llama3.1:latest" in response.data["models"]
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("llama_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_llama_response_for_prompt(self, api_client):
        payload = {
            "model": "llama3.1",
            "prompt": [
                {"index": 0, "message": "Quantos Planetas tem o sistema solar?"},
            ],
        }
        response = api_client.post(reverse("api:llama-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "llama"
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("llama_bigger_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_llama_response_for_bigger_prompt(self, api_client):
        payload = {
            "model": "llama3.1",
            "prompt": [
                {"index": 0, "message": "Quantos Planetas tem o sistema solar?"},
                {"index": 1, "message": "Considere que estamos no ano de 2005."},
            ],
        }
        response = api_client.post(reverse("api:llama-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "llama"
        assert response.status_code == status_code.HTTP_200_OK
