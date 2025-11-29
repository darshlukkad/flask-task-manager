// Task Manager JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Add priority-based styling to task items
    const taskItems = document.querySelectorAll('.task-item');
    taskItems.forEach(item => {
        const priorityBadge = item.querySelector('.badge');
        if (priorityBadge) {
            const priority = priorityBadge.textContent.toLowerCase().trim();
            item.classList.add(`${priority}-priority`);
        }
    });

    // Add smooth transitions for task completion
    const toggleButtons = document.querySelectorAll('a[href*="toggle_task"]');
    toggleButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const taskItem = this.closest('.task-item');
            if (taskItem) {
                taskItem.style.transition = 'all 0.3s ease';
            }
        });
    });

    // Form validation
    const addTaskForm = document.querySelector('form[action*="add_task"]');
    if (addTaskForm) {
        addTaskForm.addEventListener('submit', function(e) {
            const titleInput = this.querySelector('input[name="title"]');
            if (titleInput && !titleInput.value.trim()) {
                e.preventDefault();
                titleInput.focus();
                showAlert('Please enter a task title!', 'error');
            }
        });
    }

    const editTaskForm = document.querySelector('form[action*="edit_task"]');
    if (editTaskForm) {
        editTaskForm.addEventListener('submit', function(e) {
            const titleInput = this.querySelector('input[name="title"]');
            if (titleInput && !titleInput.value.trim()) {
                e.preventDefault();
                titleInput.focus();
                showAlert('Please enter a task title!', 'error');
            }
        });
    }

    // Delete confirmation
    const deleteButtons = document.querySelectorAll('a[href*="delete_task"]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
            }
        });
    });

    // Add loading state to buttons
    const submitButtons = document.querySelectorAll('button[type="submit"]');
    submitButtons.forEach(button => {
        button.addEventListener('click', function() {
            this.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status"></span>Processing...';
            this.disabled = true;
        });
    });

    // Auto-resize textareas
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });

    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Ctrl/Cmd + Enter to submit forms
        if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
            const activeForm = document.activeElement.closest('form');
            if (activeForm) {
                const submitButton = activeForm.querySelector('button[type="submit"]');
                if (submitButton) {
                    submitButton.click();
                }
            }
        }
    });
});

// Utility function to show alerts
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alertDiv, alertContainer.firstChild);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alertDiv);
        bsAlert.close();
    }, 5000);
}

// API functions for future enhancements
const TaskAPI = {
    async getTasks() {
        try {
            const response = await fetch('/api/tasks');
            return await response.json();
        } catch (error) {
            console.error('Error fetching tasks:', error);
            return [];
        }
    },

    async addTask(taskData) {
        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error adding task:', error);
            throw error;
        }
    },

    async updateTask(taskId, taskData) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(taskData)
            });
            return await response.json();
        } catch (error) {
            console.error('Error updating task:', error);
            throw error;
        }
    },

    async deleteTask(taskId) {
        try {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: 'DELETE'
            });
            return await response.json();
        } catch (error) {
            console.error('Error deleting task:', error);
            throw error;
        }
    }
};

// Export for use in other scripts
window.TaskAPI = TaskAPI;
