import base64
import operator

import filetype
from drf_extra_fields.fields import Base64FileField
from PIL import Image
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ListField,
    Serializer,
    ValidationError,
)


class GeminiBase64File(Base64FileField):
    ALLOWED_TYPES = ["png", "jpg", "mp3", "wav"]

    def get_file_extension(self, filename, decoded_file):
        extension = filetype.guess_extension(decoded_file)
        return extension


class MessageSerializer(Serializer):
    index = IntegerField()
    message = CharField(required=False, max_length=500)
    file = GeminiBase64File(required=False)

    def validate(self, data):
        if ("message" in data and "file" in data) or ("message" not in data and "file" not in data):
            raise ValidationError(
                "É necessário enviar o campo 'message' ou o campo 'file'. Não é possível enviar os 2 simultaneamente."
            )
        return data


class PromptSerializer(Serializer):
    model = CharField(required=True, allow_blank=True, max_length=100)
    prompt = ListField(child=MessageSerializer())


class ProviderResponseSerializer(Serializer):
    provider = CharField(required=True, max_length=100)
    response = CharField()


def convert_file_to_base_64(path, encoding="utf-8"):
    with open(path, "rb") as f:
        base64_bytes = base64.b64encode(f.read())
    return base64_bytes.decode(encoding)


def convert_base_64_to_file(base64_content, path):
    with open(path, "wb") as f:
        f.write(base64.b64decode(base64_content))
    return path


def preprocess_file(f):
    if f.name.endswith(".wav"):
        return {"mime_type": "audio/wav", "data": f.read()}
    if f.name.endswith(".mp3"):
        return {"mime_type": "audio/mp3", "data": f.read()}
    if f.name.endswith(".jpg") or f.name.endswith(".png"):
        return Image.open(f)
    raise Exception("Formato não suportado.")


def build_prompt_gemini(prompt):
    sorted_prompt = sorted(prompt, key=operator.itemgetter("index"))
    final_prompt = [preprocess_file(p["file"]) if "file" in p else p["message"] for p in sorted_prompt]
    return final_prompt
