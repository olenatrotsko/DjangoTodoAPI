from django.urls import path

from todos import views

urlpatterns = [
    # path('create', views.CreateTodoApiView.as_view(), name='create-todo'),
    # path('list', views.TodoListApiView.as_view(), name='list-todo'),
    path('', views.TodosApiView.as_view(), name='todos'),
    path('<int:id>', views.TodoDetailApiView.as_view(), name='todo'),
    
]
