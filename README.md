# 🚀 Flask Task Manager Web Application

A modern, responsive web application built with Flask and Bootstrap for managing tasks. Features a beautiful UI, REST API, and Docker support.

## ✨ Features

- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **Task Management**: Create, read, update, delete tasks
- **Priority Levels**: Low, Medium, High priority tasks
- **Task Completion**: Mark tasks as complete/incomplete
- **Statistics Dashboard**: View task counts and completion status
- **REST API**: Full API endpoints for programmatic access
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Health Check**: Built-in health monitoring endpoint

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome 6
- **Containerization**: Docker, Docker Compose
- **Database**: In-memory storage (easily replaceable with PostgreSQL/MySQL)

## 🚀 Quick Start

### Option 1: Using Docker (Recommended)

1. **Clone and navigate to the project:**
   ```bash
   cd flask-web-app
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Web UI: http://localhost:5000
   - API: http://localhost:5000/api/tasks
   - Health Check: http://localhost:5000/health

### Option 2: Local Development

1. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   - Web UI: http://localhost:5000

## 📁 Project Structure

```
flask-web-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Multi-container setup
├── .dockerignore         # Docker ignore file
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html       # Base template
│   ├── index.html      # Home page
│   └── edit_task.html  # Edit task page
└── static/             # Static files
    ├── css/
    │   └── style.css   # Custom styles
    └── js/
        └── app.js      # JavaScript functionality
```

## 🔌 API Endpoints

### Web Routes
- `GET /` - Main task manager page
- `POST /add_task` - Add a new task
- `GET /toggle_task/<id>` - Toggle task completion
- `GET /delete_task/<id>` - Delete a task
- `GET /edit_task/<id>` - Edit task page
- `POST /edit_task/<id>` - Update task
- `GET /health` - Health check

### API Routes
- `GET /api/tasks` - Get all tasks (JSON)
- `POST /api/tasks` - Create new task (JSON)
- `PUT /api/tasks/<id>` - Update task (JSON)
- `DELETE /api/tasks/<id>` - Delete task (JSON)

### Example API Usage

**Get all tasks:**
```bash
curl http://localhost:5000/api/tasks
```

**Create a new task:**
```bash
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn Docker", "description": "Study Docker basics", "priority": "high"}'
```

**Update a task:**
```bash
curl -X PUT http://localhost:5000/api/tasks/<task-id> \
  -H "Content-Type: application/json" \
  -d '{"completed": true}'
```

## 🐳 Docker Commands

**Build the image:**
```bash
docker build -t flask-task-manager .
```

**Run the container:**
```bash
docker run -p 5000:5000 flask-task-manager
```

**Run with Docker Compose:**
```bash
docker-compose up -d
```

**View logs:**
```bash
docker-compose logs -f
```

**Stop the application:**
```bash
docker-compose down
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to `production` for production deployment
- `SECRET_KEY`: Secret key for Flask sessions (change in production)
- `FLASK_APP`: Flask application file (default: app.py)

### Docker Environment
You can modify the environment variables in `docker-compose.yml`:
```yaml
environment:
  - FLASK_ENV=production
  - SECRET_KEY=your-secret-key-here
```

## 🎨 Customization

### Adding New Features
1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Create new templates in `templates/`
3. **Styling**: Modify `static/css/style.css`
4. **JavaScript**: Add functionality in `static/js/app.js`

### Database Integration
To add a real database (PostgreSQL/MySQL):
1. Uncomment the database service in `docker-compose.yml`
2. Install database adapter (e.g., `psycopg2` for PostgreSQL)
3. Update `app.py` to use the database instead of in-memory storage

## 🚀 Production Deployment

### Using Docker
1. **Build production image:**
   ```bash
   docker build -t your-registry/flask-task-manager:latest .
   ```

2. **Push to registry:**
   ```bash
   docker push your-registry/flask-task-manager:latest
   ```

3. **Deploy:**
   ```bash
   docker-compose -f docker-compose.prod.yml up -d
   ```

### Environment Setup
- Set `FLASK_ENV=production`
- Use a strong `SECRET_KEY`
- Configure proper database credentials
- Set up reverse proxy (Nginx) for production

## 🧪 Testing

**Run health check:**
```bash
curl http://localhost:5000/health
```

**Test API endpoints:**
```bash
# Get all tasks
curl http://localhost:5000/api/tasks

# Create a task
curl -X POST http://localhost:5000/api/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "priority": "medium"}'
```

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

If you have any questions or issues, please open an issue on GitHub.

---

**Happy Task Managing! 🎉**
