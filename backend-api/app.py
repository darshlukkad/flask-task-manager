from flask import Flask, request, jsonify
from datetime import datetime
import os
from database import db_session, init_db, shutdown_session
from models import Task

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Initialize database on startup
with app.app_context():
    try:
        init_db()
    except Exception as e:
        print(f"Database initialization error: {e}")
        print("Will retry on first request...")

# Teardown database session after each request
@app.teardown_appcontext
def shutdown_app_session(exception=None):
    shutdown_session(exception)


@app.route('/health')
def health_check():
    """Health check endpoint."""
    try:
        # Test database connection
        db_session.execute('SELECT 1')
        db_status = 'healthy'
    except Exception as e:
        db_status = f'unhealthy: {str(e)}'
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': db_status
    })


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get all tasks."""
    try:
        tasks = Task.query.all()
        return jsonify([task.to_dict() for task in tasks])
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['POST'])
def create_task():
    """Create a new task."""
    try:
        data = request.get_json()
        
        if not data or 'title' not in data:
            return jsonify({'error': 'Title is required'}), 400
        
        task = Task(
            title=data['title'],
            description=data.get('description', ''),
            priority=data.get('priority', 'medium')
        )
        
        db_session.add(task)
        db_session.commit()
        
        return jsonify(task.to_dict()), 201
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['GET'])
def get_task(task_id):
    """Get a specific task by ID."""
    try:
        task = Task.query.filter_by(id=task_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        return jsonify(task.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    """Update a task."""
    try:
        task = Task.query.filter_by(id=task_id).first()
        
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
        
        task.updated_at = datetime.utcnow()
        db_session.commit()
        
        return jsonify(task.to_dict())
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task."""
    try:
        task = Task.query.filter_by(id=task_id).first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        db_session.delete(task)
        db_session.commit()
        
        return jsonify({'message': 'Task deleted successfully'})
    except Exception as e:
        db_session.rollback()
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
