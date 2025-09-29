from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ContratoViewSet, ExpensaViewSet, MultaViewSet
from .views_payments import CreatePaymentIntentExpensa, VerifyPaymentIntentExpensa



# Router
router = DefaultRouter()
router.register(r'contratos', ContratoViewSet, basename='contratos')
router.register(r'expensas', ExpensaViewSet, basename='expensas')
router.register(r'multas', MultaViewSet, basename='multas')

urlpatterns = [
    path('', include(router.urls)),
    path("create-payment-intent/", CreatePaymentIntentExpensa.as_view()),
    path("verify-payment-intent/", VerifyPaymentIntentExpensa.as_view()),
]