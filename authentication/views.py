from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from rest_framework import response, status

from authentication.serializers import RegisterSerializer

class RegisterApiView(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return response.Response(serializers.data, status=status.HTTP_201_CREATED)
        return response.Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    

