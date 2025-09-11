from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from datetime import datetime
import uuid
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# In-memory storage for demo purposes
tasks = []

class Task:
    def __init__(self, title, description="", priority="medium"):
        self.id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.priority = priority  # low, medium, high
        self.completed = False
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'completed': self.completed,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d %H:%M')
        }

@app.route('/')
def index():
    """Main page with task list"""
    return render_template('index.html', tasks=tasks)

@app.route('/add_task', methods=['POST'])
def add_task():
    """Add a new task"""
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    priority = request.form.get('priority', 'medium')
    
    if not title:
        flash('Task title is required!', 'error')
        return redirect(url_for('index'))
    
    task = Task(title, description, priority)
    tasks.append(task)
    flash('Task added successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/toggle_task/<task_id>')
def toggle_task(task_id):
    """Toggle task completion status"""
    task = next((t for t in tasks if t.id == task_id), None)
    
    if task:
        task.completed = not task.completed
        task.updated_at = datetime.now()
        flash(f'Task "{task.title}" marked as {"completed" if task.completed else "incomplete"}!', 'info')
    else:
        flash('Task not found!', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete_task/<task_id>')
def delete_task(task_id):
    """Delete a task"""
    global tasks
    task = next((t for t in tasks if t.id == task_id), None)
    
    if task:
        tasks = [t for t in tasks if t.id != task_id]
        flash(f'Task "{task.title}" deleted successfully!', 'success')
    else:
        flash('Task not found!', 'error')
    
    return redirect(url_for('index'))

@app.route('/edit_task/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    """Edit a task"""
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        flash('Task not found!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        task.title = request.form.get('title', task.title).strip()
        task.description = request.form.get('description', task.description).strip()
        task.priority = request.form.get('priority', task.priority)
        task.updated_at = datetime.now()
        
        if not task.title:
            flash('Task title is required!', 'error')
            return render_template('edit_task.html', task=task)
        
        flash('Task updated successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('edit_task.html', task=task)

@app.route('/api/tasks')
def api_tasks():
    """API endpoint to get all tasks as JSON"""
    return jsonify([task.to_dict() for task in tasks])

@app.route('/api/tasks', methods=['POST'])
def api_add_task():
    """API endpoint to add a new task"""
    data = request.get_json()
    
    if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
    
    task = Task(
        title=data['title'],
        description=data.get('description', ''),
        priority=data.get('priority', 'medium')
    )
    
    tasks.append(task)
    return jsonify(task.to_dict()), 201

@app.route('/api/tasks/<task_id>', methods=['PUT'])
def api_update_task(task_id):
    """API endpoint to update a task"""
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    data = request.get_json()
    
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'priority' in data:
        task.priority = data['priority']
    if 'completed' in data:
        task.completed = data['completed']
    
    task.updated_at = datetime.now()
    return jsonify(task.to_dict())

@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def api_delete_task(task_id):
    """API endpoint to delete a task"""
    global tasks
    task = next((t for t in tasks if t.id == task_id), None)
    
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    tasks = [t for t in tasks if t.id != task_id]
    return jsonify({'message': 'Task deleted successfully'})

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'tasks_count': len(tasks)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
