import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL.JpegImagePlugin import JpegImageFile
from providers.serializers import (
    MessageSerializer,
    build_prompt_gemini,
    convert_base_64_to_file,
    convert_file_to_base_64,
)


def get_content(path):
    with open(path, "r") as f:
        content = f.read()
    return content.strip()


def get_content_binary(path):
    with open(path, "rb") as f:
        content = f.read()
    return content.strip()


@pytest.fixture
def nao_image():
    return "./providers/tests/assets/nao.png"


@pytest.fixture
def nao_base64():
    return get_content("./providers/tests/assets/nao.png.base64")


class TestBase64Converters:

    def test_should_convert_image_to_base_64(self, nao_image, nao_base64):
        assert convert_file_to_base_64(nao_image) == nao_base64

    def test_should_convert_base_64_to_image(self, nao_base64, tmp_path):
        new_nao_image_path = tmp_path / "nao-created.png"
        convert_base_64_to_file(base64_content=nao_base64, path=new_nao_image_path)
        assert convert_file_to_base_64(new_nao_image_path) == nao_base64


class TestMessageSerializer:

    def test_should_return_errors(self):
        message = MessageSerializer(data={})
        assert message.is_valid() is False
        assert len(message.errors) == 1
        message = MessageSerializer(data={"index": 1})
        assert message.is_valid() is False
        assert len(message.errors) == 1

    def test_should_return_valid_message_serializer_with_message(self):
        message = MessageSerializer(data={"index": 1, "message": "big-long-prompt-for-gen-ai"})
        assert message.is_valid() is True

    @pytest.mark.parametrize(
        "file_",
        [
            "./providers/tests/assets/file.jpg",
            "./providers/tests/assets/file.mp3",
            "./providers/tests/assets/file.png",
            "./providers/tests/assets/file.wav",
        ],
    )
    def test_should_return_valid_message_serializer_with_file(self, file_):
        message = MessageSerializer(data={"index": 1, "file": convert_file_to_base_64(file_)})
        assert message.is_valid() is True

    def test_should_fail_when_passing_both_message_and_file(self):
        message = MessageSerializer(
            data={
                "index": 1,
                "message": "big-long-prompt-for-gen-ai",
                "file": convert_file_to_base_64("./providers/tests/assets/file.jpg"),
            }
        )
        assert message.is_valid() is False
        assert len(message.errors) == 1


class TestPromptBuilder:

    def test_should_return_ordered_prompt(self):
        file_image = "./providers/tests/assets/file.jpg"
        file_sound = "./providers/tests/assets/file.wav"
        prompt = [
            {"index": 3, "message": "Descreva a imagem."},
            {
                "index": 1,
                "message": (
                    "O NAO é um robô humanóide considerado como um dos mais avançados robôs da atualidade. "
                    "Seu uso está vinculado ao ensino e à pesquisa em Robótica e Inteligência Artificial em"
                    " universidades e institutos de investigação. NAO também é usado para aprender ensinar "
                    "programação nas escolas.  A seguir uma foto do NAO V6."
                ),
            },
            {
                "index": 4,
                "file": SimpleUploadedFile(file_image, get_content_binary(file_image), content_type="image/jpeg"),
            },
            {
                "index": 2,
                "file": SimpleUploadedFile(file_sound, get_content_binary(file_sound), content_type="audio/wav"),
            },
        ]

        prompt_gemini = build_prompt_gemini(prompt)
        assert isinstance(prompt_gemini[0], str)
        assert prompt_gemini[1]["mime_type"] == "audio/wav"
        assert isinstance(prompt_gemini[2], str)
        assert isinstance(prompt_gemini[3], JpegImageFile)
