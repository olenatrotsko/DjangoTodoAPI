from django.shortcuts import render
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from todos.models import Todo
from todos.serializers import TodoSerializer

class CreateTodoApiView(CreateAPIView):
    
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    
class TodoListApiView(ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (IsAuthenticated,)
    queryset = Todo.objects.all()

    def get_queryset(self):
        return Todo.objects.filter(owner=self.request.user)
    