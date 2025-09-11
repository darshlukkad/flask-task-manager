import unittest
import json
from app import app as flask_app, tasks, Task

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        """Set up test client and clear tasks before each test"""
        self.app = flask_app.test_client()
        self.app.testing = True
        # Clear tasks before each test
        global tasks
        tasks.clear()
        # Reset the tasks list in the app module
        import app
        app.tasks.clear()

    def test_home_page(self):
        """Test that home page loads successfully"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Task Manager', response.data)

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')
        self.assertIn('timestamp', data)

    def test_api_get_tasks_empty(self):
        """Test API endpoint for getting tasks when empty"""
        response = self.app.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data, [])

    def test_api_create_task(self):
        """Test API endpoint for creating a task"""
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description',
            'priority': 'high'
        }
        
        response = self.app.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Test Task')
        self.assertEqual(data['description'], 'Test Description')
        self.assertEqual(data['priority'], 'high')
        self.assertFalse(data['completed'])

    def test_api_create_task_missing_title(self):
        """Test API endpoint for creating a task without title"""
        task_data = {
            'description': 'Test Description'
        }
        
        response = self.app.post('/api/tasks',
                               data=json.dumps(task_data),
                               content_type='application/json')
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_api_update_task(self):
        """Test API endpoint for updating a task"""
        # First create a task
        task = Task('Original Title', 'Original Description', 'low')
        from app import tasks as app_tasks
        app_tasks.append(task)
        
        update_data = {
            'title': 'Updated Title',
            'completed': True
        }
        
        response = self.app.put(f'/api/tasks/{task.id}',
                              data=json.dumps(update_data),
                              content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['title'], 'Updated Title')
        self.assertTrue(data['completed'])

    def test_api_delete_task(self):
        """Test API endpoint for deleting a task"""
        # First create a task
        task = Task('Task to Delete', 'This will be deleted', 'medium')
        from app import tasks as app_tasks
        app_tasks.append(task)
        
        response = self.app.delete(f'/api/tasks/{task.id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('deleted successfully', data['message'])
        
        # Verify task is actually deleted from the global tasks list
        from app import tasks
        self.assertEqual(len(tasks), 0)

    def test_api_get_nonexistent_task(self):
        """Test API endpoint for getting a non-existent task"""
        # The API doesn't have a GET endpoint for individual tasks
        # This test should check that the endpoint doesn't exist (405 Method Not Allowed)
        response = self.app.get('/api/tasks/nonexistent-id')
        self.assertEqual(response.status_code, 405)  # Method not allowed

    def test_task_class(self):
        """Test Task class functionality"""
        task = Task('Test Task', 'Test Description', 'high')
        
        self.assertEqual(task.title, 'Test Task')
        self.assertEqual(task.description, 'Test Description')
        self.assertEqual(task.priority, 'high')
        self.assertFalse(task.completed)
        self.assertIsNotNone(task.id)
        self.assertIsNotNone(task.created_at)
        
        # Test to_dict method
        task_dict = task.to_dict()
        self.assertEqual(task_dict['title'], 'Test Task')
        self.assertEqual(task_dict['priority'], 'high')
        self.assertFalse(task_dict['completed'])

    def test_web_add_task_form(self):
        """Test web form for adding a task"""
        form_data = {
            'title': 'Web Form Task',
            'description': 'Added via web form',
            'priority': 'medium'
        }
        
        response = self.app.post('/add_task', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that task was added to the global tasks list
        from app import tasks as app_tasks
        self.assertEqual(len(app_tasks), 1)
        self.assertEqual(app_tasks[0].title, 'Web Form Task')

    def test_web_add_task_missing_title(self):
        """Test web form validation for missing title"""
        form_data = {
            'description': 'No title provided',
            'priority': 'medium'
        }
        
        response = self.app.post('/add_task', data=form_data, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Check that no task was added
        self.assertEqual(len(tasks), 0)

if __name__ == '__main__':
    unittest.main()
