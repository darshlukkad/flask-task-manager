# 🚀 Flask Task Manager Web Application

A modern, responsive web application built with Flask and Bootstrap for managing tasks. Features a beautiful UI, REST API, and Docker support.

## ⚡ One-Command Start

**Get started in seconds with Docker:**

```bash
docker run -p 5000:5000 darshlukkad3110/flask-task-manager:latest
```

Then visit http://localhost:5000 🚀

## ✨ Features

- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **Task Management**: Create, read, update, delete tasks
- **Priority Levels**: Low, Medium, High priority tasks
- **Task Completion**: Mark tasks as complete/incomplete
- **Statistics Dashboard**: View task counts and completion status
- **REST API**: Full API endpoints for programmatic access
- **Docker Support**: Easy deployment with Docker and Docker Compose
- **Testing Suite**: Comprehensive unit tests with 69% coverage
- **CI/CD Ready**: Multi-stage Docker builds with test automation
- **Health Check**: Built-in health monitoring endpoint

## 🛠️ Tech Stack

- **Backend**: Python 3.11, Flask 2.3.3
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Icons**: Font Awesome 6
- **Testing**: pytest, pytest-cov, coverage
- **Containerization**: Docker, Docker Compose (multi-stage builds)
- **Database**: In-memory storage (easily replaceable with PostgreSQL/MySQL)

## 🚀 Quick Start

### Option 1: Using Docker Hub (Fastest - No Build Required)

**Run directly from Docker Hub without cloning or building:**

```bash
# Run the latest version
docker run -p 5000:5000 darshlukkad3110/flask-task-manager:latest

# Or run the specific version
docker run -p 5000:5000 darshlukkad3110/flask-task-manager:v1.0.0
```

**Access the application:**
- Web UI: http://localhost:5000
- API: http://localhost:5000/api/tasks
- Health Check: http://localhost:5000/health

### Option 2: Using Docker Compose (Local Development)

1. **Clone and navigate to the project:**
   ```bash
   git clone https://github.com/darshlukkad/flask-task-manager.git
   cd flask-task-manager
   ```

2. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

3. **Access the application:**
   - Web UI: http://localhost:5000
   - API: http://localhost:5000/api/tasks
   - Health Check: http://localhost:5000/health

### Option 3: Local Development (Python)

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
├── test_app.py           # Unit tests
├── requirements.txt       # Python dependencies
├── pytest.ini           # Test configuration
├── Makefile             # Development commands
├── Dockerfile            # Multi-stage Docker configuration
├── docker-compose.yml    # Multi-container setup
├── .dockerignore         # Docker ignore file
├── .gitignore           # Git ignore rules
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

## 🐳 Docker Hub

### Available Images

Our Flask Task Manager is available on Docker Hub:

- **Latest Version**: `darshlukkad3110/flask-task-manager:latest`
- **Versioned**: `darshlukkad3110/flask-task-manager:v1.0.0`

**Docker Hub Repository**: [hub.docker.com/r/darshlukkad3110/flask-task-manager](https://hub.docker.com/r/darshlukkad3110/flask-task-manager)

### Quick Docker Commands

**Run from Docker Hub (Recommended):**
```bash
# Run the latest version
docker run -p 5000:5000 darshlukkad3110/flask-task-manager:latest

# Run in background
docker run -d -p 5000:5000 --name flask-app darshlukkad3110/flask-task-manager:latest

# Run with custom port
docker run -p 8080:5000 darshlukkad3110/flask-task-manager:latest
```

**Local Development Commands:**
```bash
# Build the image locally
docker build -t flask-task-manager .

# Run locally built container
docker run -p 5000:5000 flask-task-manager

# Run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

**Container Management:**
```bash
# View running containers
docker ps

# Stop container
docker stop flask-app

# Remove container
docker rm flask-app

# View container logs
docker logs flask-app

# Execute commands in running container
docker exec -it flask-app /bin/bash
```

## 🧪 Testing

### Running Tests

**Option 1: Docker Compose (Recommended)**
```bash
# Run all tests
docker-compose run --rm test

# Run tests with coverage
docker-compose run --rm test-coverage

# Run specific test
docker-compose run --rm test python -m pytest test_app.py::TestTaskManager::test_home_page -v
```

**Option 2: Make Commands**
```bash
# Run tests in Docker
make docker-test

# Run tests with coverage
make docker-test-coverage

# Run tests locally (requires Python environment)
make test

# Run tests with coverage locally
make test-coverage
```

**Option 3: Direct Docker Commands**
```bash
# Build test image
docker build --target test -t flask-task-manager-test .

# Run tests
docker run --rm flask-task-manager-test

# Run tests with coverage
docker run --rm flask-task-manager-test python -m pytest test_app.py --cov=app --cov-report=term-missing
```

### Test Coverage

- **Total Coverage**: 69%
- **Test Count**: 11 tests
- **Execution Time**: ~0.11 seconds
- **Coverage Report**: Available in `htmlcov/` directory

### Test Categories

- ✅ **Web Routes**: Home page, forms, redirects
- ✅ **API Endpoints**: CRUD operations, error handling
- ✅ **Task Class**: Object creation, serialization
- ✅ **Form Validation**: Input validation, error messages
- ✅ **Health Checks**: System monitoring endpoints

### CI/CD Integration

The project is ready for continuous integration with:
- **GitHub Actions**
- **GitLab CI**
- **Jenkins**
- **Azure DevOps**

Example GitHub Actions workflow:
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: docker-compose run --rm test
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

## 🛠️ Development

### Available Commands

**Using Make (Recommended):**
```bash
# Development
make install          # Install dependencies
make run             # Run application locally
make test            # Run tests locally
make test-coverage   # Run tests with coverage

# Docker
make docker-build    # Build Docker image
make docker-run      # Run Docker container
make docker-test     # Run tests in Docker
make docker-up       # Start all services
make docker-down     # Stop all services

# Cleanup
make clean           # Clean temporary files
```

**Using Docker Compose:**
```bash
# Development
docker-compose up --build          # Start application
docker-compose run --rm test       # Run tests
docker-compose run --rm test-coverage  # Run tests with coverage
docker-compose down                # Stop services
```

### Adding New Features
1. **Backend**: Add new routes in `app.py`
2. **Frontend**: Create new templates in `templates/`
3. **Styling**: Modify `static/css/style.css`
4. **JavaScript**: Add functionality in `static/js/app.js`
5. **Tests**: Add tests in `test_app.py`

### Database Integration
To add a real database (PostgreSQL/MySQL):
1. Uncomment the database service in `docker-compose.yml`
2. Install database adapter (e.g., `psycopg2` for PostgreSQL)
3. Update `app.py` to use the database instead of in-memory storage
4. Add database tests to `test_app.py`

## 🚀 Production Deployment

### Option 1: Deploy from Docker Hub (Easiest)

**Deploy directly from Docker Hub without building:**

```bash
# Deploy latest version
docker run -d -p 5000:5000 --name flask-task-manager \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret-key \
  --restart unless-stopped \
  darshlukkad3110/flask-task-manager:latest

# Deploy specific version
docker run -d -p 5000:5000 --name flask-task-manager \
  -e FLASK_ENV=production \
  -e SECRET_KEY=your-production-secret-key \
  --restart unless-stopped \
  darshlukkad3110/flask-task-manager:v1.0.0
```

### Option 2: Deploy with Docker Compose

1. **Create production docker-compose.yml:**
   ```yaml
   version: '3.8'
   services:
     web:
       image: darshlukkad3110/flask-task-manager:latest
       ports:
         - "5000:5000"
       environment:
         - FLASK_ENV=production
         - SECRET_KEY=your-production-secret-key
       restart: unless-stopped
       healthcheck:
         test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
         interval: 30s
         timeout: 10s
         retries: 3
   ```

2. **Deploy:**
   ```bash
   docker-compose up -d
   ```

### Option 3: Build and Deploy Locally

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

### Production Environment Setup
- Set `FLASK_ENV=production`
- Use a strong `SECRET_KEY`
- Configure proper database credentials
- Set up reverse proxy (Nginx) for production
- Use Docker secrets for sensitive data
- Set up monitoring and logging

## 🔍 Manual Testing

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

> **Note**: For automated testing, see the [Testing section](#-testing) above.

## 📈 Performance

| Metric              | Container (Docker) | VM (Vagrant) |
|---------------------|--------------------|--------------|
| Cold start          | 3692 ms            | 12444 ms     |
| Memory usage        | 51.9 MB            | 267.8 MB     |
| App response time   | 0.2 ms             | 5.2 ms       |

**Test environment:**

- Host: macOS (Apple Silicon, arm64)
- VM: Ubuntu 24.02 via Multipass
- Container runtime: Docker

**Metrics explained:**

- Cold start: Time from starting the app process until the first successful HTTP response.
- Memory usage: Approximate resident memory of the running app process in steady state.
- App response time: Typical request latency for a simple endpoint under light load.

**Why the differences:**

- Containers share the host kernel and have minimal userspace, so startup and memory footprints are smaller than full VMs.
- The VM runs a full Ubuntu OS (system services, background daemons), which increases baseline memory and can lengthen cold starts.
- Additional virtualization layers and I/O in the VM add latency; containers have fewer layers between the app and the host.
- On macOS arm64, Docker uses native virtualization but still benefits from lightweight container images; Multipass Ubuntu has more packages and services enabled by default.
- Network path in VMs can involve extra virtual NICs and NAT; the container path is typically simpler, yielding lower per-request overhead.

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
