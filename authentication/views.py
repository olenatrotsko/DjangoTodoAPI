from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions

from authentication.serializers import LoginSerializer, RegisterSerializer

class AuthUserApiView(GenericAPIView):
        
        permission_classes = (permissions.IsAuthenticated,  )
    
        def get(self, request):
            user = request.user
            serializer = RegisterSerializer(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)

class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status=status.HTTP_201_CREATED)
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginApiView(GenericAPIView):

    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)

        user = authenticate(email=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return response.Response(serializer.data, status=status.HTTP_200_OK)
        return response.Response({'message':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
