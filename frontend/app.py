from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
import requests
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Backend API URL from environment variable
BACKEND_API_URL = os.environ.get('BACKEND_API_URL', 'http://backend-api:5000')


def get_tasks():
    """Fetch all tasks from backend API."""
    try:
        response = requests.get(f'{BACKEND_API_URL}/api/tasks', timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching tasks: {e}")
        return []


@app.route('/')
def index():
    """Main page with task list."""
    tasks = get_tasks()
    return render_template('index.html', tasks=tasks)


@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task."""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium')
    
    if not title:
        flash('Task title is required!', 'error')
        return redirect(url_for('index'))
    
    try:
        response = requests.post(
            f'{BACKEND_API_URL}/api/tasks',
            json={
                'title': title,
                'description': description,
                'priority': priority
            },
            timeout=5
        )
        response.raise_for_status()
        flash('Task added successfully!', 'success')
    except requests.exceptions.RequestException as e:
        flash(f'Error adding task: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/toggle_task/<task_id>')
def toggle_task(task_id):
    """Toggle task completion status."""
    try:
        # Get current task
        response = requests.get(f'{BACKEND_API_URL}/api/tasks/{task_id}', timeout=5)
        response.raise_for_status()
        task = response.json()
        
        # Toggle completion
        response = requests.put(
            f'{BACKEND_API_URL}/api/tasks/{task_id}',
            json={'completed': not task['completed']},
            timeout=5
        )
        response.raise_for_status()
        
        status = 'completed' if not task['completed'] else 'incomplete'
        flash(f'Task "{task["title"]}" marked as {status}!', 'info')
    except requests.exceptions.RequestException as e:
        flash(f'Error toggling task: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    """Delete a task."""
    try:
        # Get task first for flash message
        response = requests.get(f'{BACKEND_API_URL}/api/tasks/{task_id}', timeout=5)
        if response.status_code == 200:
            task = response.json()
            title = task.get('title', 'Task')
        else:
            title = 'Task'
        
        # Delete task
        response = requests.delete(f'{BACKEND_API_URL}/api/tasks/{task_id}', timeout=5)
        response.raise_for_status()
        
        flash(f'Task "{title}" deleted successfully!', 'success')
    except requests.exceptions.RequestException as e:
        flash(f'Error deleting task: {str(e)}', 'error')
    
    return redirect(url_for('index'))


@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task."""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        description = request.form.get('description', '').strip()
        priority = request.form.get('priority', 'medium')
        
        if not title:
            flash('Task title is required!', 'error')
            return redirect(url_for('edit_task', task_id=task_id))
        
        try:
            response = requests.put(
                f'{BACKEND_API_URL}/api/tasks/{task_id}',
                json={
                    'title': title,
                    'description': description,
                    'priority': priority
                },
                timeout=5
            )
            response.raise_for_status()
            flash('Task updated successfully!', 'success')
            return redirect(url_for('index'))
        except requests.exceptions.RequestException as e:
            flash(f'Error updating task: {str(e)}', 'error')
    
    # GET request - fetch task
    try:
        response = requests.get(f'{BACKEND_API_URL}/api/tasks/{task_id}', timeout=5)
        response.raise_for_status()
        task = response.json()
        return render_template('edit_task.html', task=task)
    except requests.exceptions.RequestException as e:
        flash(f'Error fetching task: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/health')
def health_check():
    """Health check endpoint."""
    # Check backend connectivity
    try:
        response = requests.get(f'{BACKEND_API_URL}/health', timeout=3)
        backend_status = 'healthy' if response.status_code == 200 else 'unhealthy'
    except:
        backend_status = 'unhealthy'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'backend': backend_status
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
