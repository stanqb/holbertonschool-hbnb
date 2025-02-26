# HBnB Application

This project is a Flask-based API application for managing users, places, reviews, and amenities. The project is structured to ensure modularity, maintainability, and scalability. It uses an in-memory repository to handle object storage and validation, which will later be replaced by a database-backed solution.

## Project Structure


- app/: Contains the core application code.
- api/: Houses the API endpoints, organized by version (v1/).
- models/: Contains the business logic classes (ex, user.py, place.py).
- services/: Implements the Facade pattern, managing the interaction between layers.
- persistence/: Implements the in-memory repository, which will later be replaced by a database-backed solution using SQL Alchemy.
- run.py: Entry point for running the Flask application.
- config.py: Application settings.
- requirements.txt: Lists all the Python packages needed for the project.
- README.md: Contains a brief overview of the project.

## How to run the application

1. Clone the repository:
git clone (URL of the repo)

2. Install dependencies (conseilled to use a virtual environnement):
pip install -r requirements.txt

3. Run the application:
python3 run.py
