from rest_framework import viewsets,status
from .models import User, Garage, Service, Booking, Payment, Review
from .serializers import (RegisterSerializer, GarageSerializer, ServiceSerializer, BookingSerializer, PaymentSerializer, ReviewSerializer)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

class RegisterViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class DashboardViewset(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "message": f"Welcome {user.username}!",
            "email": user.email,
            "name": f"{user.first_name} {user.last_name}"
        })

class GarageViewSet(viewsets.ModelViewSet):
    queryset = Garage.objects.all()
    serializer_class = GarageSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    
'''
    def send_booking_email(user_email, garage_name):
        subject = 'Booking Confirmation'
        message = f'Your booking for garage "{garage_name}" has been confirmed. Thank you!'
        from_email = 'karthika271@gmail.com'
        recipient_list = [user_email]

        send_mail(subject, message, from_email, recipient_list)'''


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    
    
class ForgotPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"http://localhost:5173/reset-password/{uid}/{token}/"

        send_mail(
            subject="Reset Your Password",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=None,
            recipient_list=[user.email],
        )

        return Response({"message": "Password reset link sent to your email"})

# Reset Password View
class ResetPasswordView(APIView):
    def post(self, request, uidb64, token):
        password = request.data.get("password")
        password2 = request.data.get("password2")

        if password != password2:
            return Response({"error": "Passwords do not match"}, status=400)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return Response({"error": "Invalid link"}, status=400)

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Invalid or expired token"}, status=400)

        user.set_password(password)
        user.save()

        return Response({"message": "Password has been reset successfully"})
