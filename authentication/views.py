import pybreaker
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterUserSerializer, UserSerializer
from .permissions import IsAdmin
from breaker.circuit_breaker import auth_breaker

class RegisterUserView(APIView):
    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterWarehouseAssistantView(APIView):
    #permission_classes = [IsAdmin]

    def post(self, request):
        data = request.data.copy()
        data['role'] = 'warehouse_assistant'  # Forzamos el rol
        serializer = RegisterUserSerializer(data=data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "Warehouse Assistant registered successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    @auth_breaker
    def authenticate_user(self, email, password):
        user = User.objects.get(email=email)
        if user.check_password(password):
            return user
        raise User.DoesNotExist  # Para manejar credenciales incorrectas

    def post(self, request):        
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = self.authenticate_user(email, password)
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
        except pybreaker.CircuitBreakerError:
            return Response({"error": "Service temporarily unavailable. Please try again later."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)