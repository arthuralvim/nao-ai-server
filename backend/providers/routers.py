from providers.views import GeminiViewSet, ProvidersViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"providers", ProvidersViewSet, basename="providers")
router.register(r"provider/gemini", GeminiViewSet, basename="gemini")