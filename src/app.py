"""
High School Management System API

A super simple FastAPI application that allows students to view and sign up
for extracurricular activities at Mergington High School.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

# Support running both as a package (python -m src.app) and directly
try:
    # When executed as a package this will work
    from .backend import routers, database
except Exception:
    # When executed directly (python src/app.py) the relative import fails.
    # Add the src directory to sys.path and import the backend package.
    import sys

    src_dir = os.path.dirname(__file__)
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)

    from backend import routers, database

# Initialize web host
app = FastAPI(
    title="Mergington High School API",
    description="API for viewing and signing up for extracurricular activities"
)

# Initialize database with sample data if empty (don't crash app if MongoDB down)
try:
    database.init_database()
except Exception:
    # Delay failure: log a warning and continue so the app can start in dev
    import logging

    logging.getLogger("uvicorn.error").warning("Could not initialize database; MongoDB may be unavailable.")

# Mount the static files directory for serving the frontend
current_dir = Path(__file__).parent
app.mount("/static", StaticFiles(directory=os.path.join(current_dir, "static")), name="static")

# Root endpoint to redirect to static index.html
@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")

# Include routers
app.include_router(routers.activities.router)
app.include_router(routers.auth.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
