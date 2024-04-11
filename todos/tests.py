from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from todos.models import Todo


class TodosAPITestCase(APITestCase):

    def create_todo(self):
        sample_todo = {'title': 'Test Todo', 'description': 'Test Description'}
        response = self.client.post(reverse('todos'), sample_todo)
        return response
   

    def authenticate(self):
        self.client.post(reverse("register"), {
           "username": "testuser", 
           "email":"test@email.com", 
           "password": "password123"})
        
        response = self.client.post(reverse("login"), {
            "email": "test@email.com", 
            "password": "password123"})
        
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['token']}")


class TestListCreateTodos(TodosAPITestCase):
      
    def test_should_not_create_todo_without_auth(self):
        response = self.create_todo()
        self.assertFalse(Todo.objects.exists())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_should_create_todo(self):
        self.authenticate()
        previous_todo_count = Todo.objects.all().count()
        response = self.create_todo()
        self.assertTrue(Todo.objects.exists())
        self.assertEqual(Todo.objects.all().count(), previous_todo_count + 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Todo')
        self.assertEqual(response.data['description'], 'Test Description')


    def test_retrieves_all_todos(self):
        self.authenticate()
        response = self.client.get(reverse('todos'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'], list)

        self.create_todo()
        response = self.client.get(reverse('todos'))
        self.assertIsInstance(response.data['count'], int)
        self.assertEqual(response.data['count'], 1)


class TestTodoDetailAPIView(TodosAPITestCase):
        
    def test_retrieves_one_todo(self):
        self.authenticate()
        response = self.create_todo()
        res = self.client.get(reverse('todo', kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        
        todo = Todo.objects.get(id=response.data['id'])
        self.assertEqual(res.data['title'], todo.title)


    def test_updates_one_todo(self):
        self.authenticate()
        response = self.create_todo()

        res = self.client.patch(reverse('todo', kwargs={'id': response.data['id']}), 
                                        {'title': 'Updated Title', 
                                         'description': 'Updated Description',
                                         'is_completed': True})
        
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        updated_todo = Todo.objects.get(id=response.data['id'])

        self.assertEqual(updated_todo.title, 'Updated Title')
        self.assertEqual(updated_todo.description, 'Updated Description')
        self.assertEqual(updated_todo.is_completed, True)


    def test_deletes_one_todo(self):
        self.authenticate()
        response = self.create_todo()
        previous_todo_count = Todo.objects.all().count()
        self.assertGreater(previous_todo_count, 0)

        res = self.client.delete(reverse('todo', kwargs={'id': response.data['id']}))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Todo.objects.exists())
