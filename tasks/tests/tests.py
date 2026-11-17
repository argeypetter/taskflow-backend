from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Task

class TaskAPITests(APITestCase):

    def setUp(self):
        # Datos iniciales o configuración que se ejecuta antes de cada test
        self.task_data = {'nombre': 'Aprender Django REST Framework', 
                          'descripcion': 'Python','Prioridad':'3',
                          'estado':'1'}
        self.create_url = reverse('task-list')  # Nombre de la ruta (URL name)

    def test_create_task(self):
        """
        Asegura que podemos crear una nueva tarea mediante POST.
        """
        response = self.client.post(self.create_url, self.task_data, format='json')
        
        # Verificar que el código de estado HTTP sea 201 (Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # Verificar que se haya creado 1 objeto en la base de datos
        self.assertEqual(Task.objects.count(), 1)
        
        # Verificar que el título coincida con el enviado
        self.assertEqual(Task.objects.get().nombre, 'Aprender Django REST Framework')

    def test_get_tasks_list(self):
        """
        Asegura que podemos obtener la lista de tareas mediante GET.
        """
        Task.objects.create(nombre='Tarea de prueba 1')
        Task.objects.create(nombre='Tarea de prueba 2')

        response = self.client.get(self.create_url)
        
        # Verificar código 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar que la respuesta contenga los 2 elementos
        self.assertEqual(len(response.data), 2)

    def test_update_task(self):
        task = Task.objects.create(nombre ='Aprender Django REST Framework', 
                          descripcion= 'Python',prioridad = '3',
                          estado = '1')
        # Construimos la URL pasando el identificador en kwargs
        url = reverse('task-detail', kwargs={'pk': task.pk})
        
        # Datos a actualizar parcialmente
        data = {'descripcion': 'es una potente y flexible biblioteca construida sobre el framework web Django'}
        
        # Ejecutamos la petición PATCH
        response = self.client.patch(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.descripcion, 'es una potente y flexible biblioteca construida sobre el framework web Django')

    def test_delete_task(self):
        task = Task.objects.create(nombre ='Aprender Django REST Framework', 
                                  descripcion= 'Python',prioridad = '3',
                                  estado = '1')
                # Construimos la URL pasando el identificador en kwargs
        url = reverse('task-detail', kwargs={'pk': task.pk})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(pk=task.pk).exists())

    def test_create_task_invalid_data(self):

        # 1. Utiliza la URL de creación
        url = reverse('task-list')

        # 2. Crea un diccionario sin el campo obligatorio nombre
        data = {
            'descripcion': 'Python',
            'prioridad': '3',
            'estado': '1'
        }

        # 3. Ejecuta la petición POST
        response = self.client.post(url, data, format='json')

        # 4. Comprueba el código HTTP
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 5. Comprueba que no se creó ningún registro
        self.assertEqual(Task.objects.count(), 0)