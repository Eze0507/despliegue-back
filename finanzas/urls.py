from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet, ExpensaViewSet, MultaViewSet
from .views_payments import CreatePaymentIntentExpensa, VerifyPaymentIntentExpensa
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet


# Router
router = DefaultRouter()
router.register(r'contratos', ContratoViewSet, basename='contratos')
router.register(r'expensas', ExpensaViewSet, basename='expensas')
router.register(r'multas', MultaViewSet, basename='multas')
router.register(r'devices', FCMDeviceAuthorizedViewSet, basename='devices')

urlpatterns = [
    path('', include(router.urls)),
    path("create-payment-intent/", CreatePaymentIntentExpensa.as_view()),
    path("verify-payment-intent/", VerifyPaymentIntentExpensa.as_view()),
]