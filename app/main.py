# app/main.py

import sqlite3
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=BASE_DIR / "templates")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

DB_PATH = BASE_DIR / "todo.db"


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS todos")
    cur.execute(
        """
        CREATE TABLE todos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            completed BOOLEAN NOT NULL CHECK (completed IN (0,1)) DEFAULT 0
        )
    """
    )
    conn.commit()
    conn.close()


# Initialize DB on startup
init_db()


@app.get("/", response_class=HTMLResponse)
def read_todos_html(request: Request):
    conn = get_db_connection()
    todos = conn.execute("SELECT * FROM todos").fetchall()
    conn.close()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "todos": todos}
    )


@app.post("/add")
def add_todo(title: str = Form(...), description: str = Form("")):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO todos (title, description, completed) VALUES (?, ?, ?)",
        (title, description, 0),
    )
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)


@app.post("/complete/{todo_id}")
def complete_todo(todo_id: int):
    conn = get_db_connection()
    cur = conn.execute(
        "UPDATE todos SET completed = 1 WHERE id = ?", (todo_id,)
    )
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{todo_id}")
def delete_todo(todo_id: int):
    conn = get_db_connection()
    conn.execute("DELETE FROM todos WHERE id = ?", (todo_id,))
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)


@app.get("/edit/{todo_id}", response_class=HTMLResponse)
def edit_todo_form(todo_id: int, request: Request):
    conn = get_db_connection()
    todo = conn.execute(
        "SELECT * FROM todos WHERE id = ?", (todo_id,)
    ).fetchone()
    conn.close()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse(
        "edit.html", {"request": request, "todo": todo}
    )


@app.post("/update/{todo_id}")
def update_todo(
    todo_id: int,
    title: str = Form(...),
    description: str = Form("")
):
    conn = get_db_connection()
    cur = conn.execute(
        "UPDATE todos SET title = ?, description = ? WHERE id = ?",
        (title, description, todo_id),
    )
    if cur.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Todo not found")
    conn.commit()
    conn.close()
    return RedirectResponse(url="/", status_code=303)
