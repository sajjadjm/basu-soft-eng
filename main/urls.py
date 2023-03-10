from rest_framework import routers

from main.views import (
    AuthViewSet,
    RefreeViewSet,
    ThesisViewSet,
    MessageViewSet,
    UserViewSet,
)

router = routers.DefaultRouter()

router.register(r"auth", AuthViewSet, basename="auth_viewset")
router.register(r"user", UserViewSet, basename="user_viewset")
router.register(r"refree", RefreeViewSet, basename="refree_viewset")
router.register(r"thesis", ThesisViewSet, basename="thesis_viewset")
router.register(r"message", MessageViewSet, basename="message_viewset")

urlpatterns = [] + router.urls
