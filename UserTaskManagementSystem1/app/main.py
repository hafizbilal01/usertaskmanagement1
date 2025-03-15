from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.database import engine, Base, get_db
from app.routes import users, tasks
from app.models import Task

# Initialize FastAPI app
app = FastAPI()

# Create database tables
Base.metadata.create_all(bind=engine)

# Configure Jinja2 Templates
templates = Jinja2Templates(directory=".app/templates")

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include API routes
app.include_router(users.router)
app.include_router(tasks.router)


# ✅ Fix the /dashboard Route
@app.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db)):
    try:
        tasks = db.query(Task).all()  # Fetch all tasks from the database
    except Exception as e:
        print(f"Database error: {e}")  # Log the error in the terminal
        tasks = []  # Prevent crashing by returning an empty list

    return templates.TemplateResponse("dashboard.html", {"request": request, "tasks": tasks, "username": "User"})
