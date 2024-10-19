from django.contrib.auth import authenticate
from rest_framework import generics, status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import *
from .tokens import create_jwt_pair_for_user
from .models import *
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

#Authenticate with JWT
class SignUpView(generics.GenericAPIView):
    serializer_class = SignUpSerializer
    permission_classes = []
    
    def post(self, request: Request):
        data = request.data

        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {"message": "User Created Successfully", "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        logger.debug("Login attempt")
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            logger.debug("Invalid email or password")
            return Response(data={"message": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

        tokens = create_jwt_pair_for_user(user)
        response = {"message": "Login Successful", "tokens": tokens}
        logger.debug("Login successful")
        return JsonResponse(response, status=status.HTTP_200_OK)

    def get(self, request):
        content = {"user": str(request.user), "auth": str(request.auth)}
        return Response(data=content, status=status.HTTP_200_OK)

class UserListAPIView(generics.ListAPIView):
    serializer_class = UserListSerializer
    permission_classes = [permissions.IsAuthenticated]
    paginator = None
    
    def get_queryset(self):
        user = self.request.user
        queryset = User.objects.filter(id=user.id)
        return queryset

@api_view(['POST'])
@permission_classes([AllowAny]) 
def GenerateApikey(request):
    if request.method == 'POST':
        name = request.data.get("name")
        if not name:
            return Response(data={"message": "Name is required"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            api_key, key = APIKey.objects.create_key(name=name)
        if not key:
            return Response(data={"message": "Failed to generate API key"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = {"message": "Generated Successfully", "api_key": key}
        return Response(data=response, status=status.HTTP_200_OK)
    return Response(data={"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)