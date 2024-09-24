import pytest
from django.urls import reverse
from providers.serializers import convert_file_to_base_64
from rest_framework import status as status_code


class TestProviders:

    def test_should_return_available_providers(self, api_client):
        response = api_client.get(reverse("api:providers-list"))
        assert response.data["providers"] == ["gemini", "openai", "llama"]
        assert response.status_code == status_code.HTTP_200_OK


class TestProviderGemini:

    def test_should_return_correct_url(self):
        assert reverse("api:gemini-status") == "/provider/gemini/status/"
        assert reverse("api:gemini-models") == "/provider/gemini/models/"
        assert reverse("api:gemini-prompt") == "/provider/gemini/prompt/"

    @pytest.mark.default_cassette("gemini_status_off.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_status_off(self, api_client, settings):
        settings.GEMINI_API_KEY = None
        response = api_client.get(reverse("api:gemini-status"))
        assert response.status_code == status_code.HTTP_503_SERVICE_UNAVAILABLE

    @pytest.mark.default_cassette("gemini_status_on.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_status_on(self, api_client):
        response = api_client.get(reverse("api:gemini-status"))
        assert response.data == {"status": "running"}
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("gemini_models.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_models(self, api_client):
        response = api_client.get(reverse("api:gemini-models"))
        assert "gemini-1.5-flash" in response.data["models"]
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("gemini_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_response_for_prompt(self, api_client):
        payload = {
            "model": "gemini-1.5-flash",
            "prompt": [
                {"index": 0, "message": "Quantos Planetas tem o sistema solar?"},
            ],
        }
        response = api_client.post(reverse("api:gemini-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "gemini"
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("gemini_bigger_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_response_for_bigger_prompt(self, api_client):
        payload = {
            "model": "gemini-1.5-flash",
            "prompt": [
                {"index": 0, "message": "Quantos Planetas tem o sistema solar?"},
                {"index": 1, "message": "Considere que estamos no ano de 2005."},
            ],
        }
        response = api_client.post(reverse("api:gemini-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "gemini"
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("gemini_image_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_response_for_image_prompt(self, api_client):
        file_ = "./providers/tests/assets/saturn.jpg"
        payload = {
            "model": "gemini-1.5-flash",
            "prompt": [
                {"index": 1, "file": convert_file_to_base_64(file_)},
                {
                    "index": 2,
                    "message": (
                        "Qual o planeta da image e quantos planetas tem o sistema solar? "
                        "Considere que estamos no ano de 2005."
                    ),
                },
            ],
        }
        response = api_client.post(reverse("api:gemini-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "gemini"
        assert response.status_code == status_code.HTTP_200_OK

    @pytest.mark.default_cassette("gemini_sound_prompt.yaml")
    @pytest.mark.vcr
    def test_should_return_gemini_response_for_sound_prompt(self, api_client):
        file_ = "./providers/tests/assets/translate.wav"
        payload = {
            "model": "gemini-1.5-flash",
            "prompt": [
                {"index": 1, "file": convert_file_to_base_64(file_)},
                {"index": 2, "message": "Traduza o som para português do Brasil e retorna a transcrição."},
            ],
        }
        response = api_client.post(reverse("api:gemini-prompt"), payload, format="json")
        assert response.data["response"] is not None
        assert response.data["provider"] == "gemini"
        assert response.status_code == status_code.HTTP_200_OK
