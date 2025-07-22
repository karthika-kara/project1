from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import  DashboardViewset, RegisterViewset, GarageViewSet, ServiceViewSet, BookingViewSet, PaymentViewSet, ReviewViewSet 
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
router = DefaultRouter()
router.register(r'users', RegisterViewset)
router.register(r'garages', GarageViewSet)
router.register(r'services', ServiceViewSet)
router.register(r'bookings', BookingViewSet)
router.register(r'payments', PaymentViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('dashboard/', DashboardViewset.as_view(), name='dashboard'),
    ]