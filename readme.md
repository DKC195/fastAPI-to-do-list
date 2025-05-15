# 📝 FastAPI To-Do App with SQLite

This is a simple to-do list web application built with FastAPI, Jinja2 templates, and Python 3. It uses SQLite for persistent task storage which resets every time the app restarts. Users can add, update, complete, and delete tasks via a web UI.

The project includes basic testing with `pytest`, Docker containerization, and GitHub Actions setup for CI (linting, testing, Docker build).

To run locally, clone the repo, set up a virtual environment, install dependencies, and launch with Uvicorn:

```bash
git clone https://github.com/yourusername/fastapi-to-do-list.git
cd fastapi-to-do-list
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run tests with:
```bash
PYTHONPATH=. pytest
```

## Build and run with Docker:
```bash
docker build -t fastapi-todo-app .
docker run -d -p 8000:8000 fastapi-todo-app
```

This app is structured with clear separation of logic (`app/`), tests (`tests/`), and configuration files (`Dockerfile`, `.github/workflows`). The GitHub Actions workflow performs linting, testing, and builds the Docker image on every push.

The UI is rendered server-side using Jinja2 templates. Tasks are persisted in a temporary SQLite database stored in-memory, which resets whenever the app restarts. This keeps the simplicity of no permanent database while allowing data persistence during a single run.