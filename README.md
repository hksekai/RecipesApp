# Recipe App

A Flask web application that suggests recipes based on ingredients using TheMealDB API. Features user session tracking and recipe history.

## Features

- Search recipes by main ingredient
- User session tracking with unique IDs
- Recipe viewing history
- SQLite database for data persistence

## Prerequisites

- Python 3.10 or higher
- pip (Python package manager)

## Installation

1. **Clone the repository:**
   ```bash
   git clone git@github.com:hksekai/RecipesApp.git
   cd RecipeApp
   ```

2. **Create and activate a virtual environment:**

   **On Windows (PowerShell):**
   ```powershell
   python -m venv recipe-app-venv
   recipe-app-venv\Scripts\activate
   ```

   **On Windows (Command Prompt):**
   ```cmd
   python -m venv recipe-app-venv
   recipe-app-venv\Scripts\activate.bat
   ```

   **On macOS/Linux:**
   ```bash
   python3 -m venv recipe-app-venv
   source recipe-app-venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Option 1: Using Flask CLI (Recommended)

With the virtual environment activated:

```bash
flask --app src.app run
```

To run in debug mode:
```bash
flask --app src.app run --debug
```

To run on a specific port:
```bash
flask --app src.app run --port 8080
```

### Option 2: Using Python Module

```bash
python -m flask --app src.app run
```

### Option 3: Using Virtual Environment Python Directly (Windows)

If not activating the virtual environment:

```powershell
recipe-app-venv\Scripts\python -m flask --app src.app run
```

### Option 4: Production Mode with Gunicorn

```bash
gunicorn "src.app:app" --bind 0.0.0.0:8000
```

## Environment Variables (Optional)

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_DEBUG` | Enable debug mode | `0` |

Set on Windows PowerShell:
```powershell
$env:FLASK_DEBUG = "1"
```

Set on Windows Command Prompt:
```cmd
set FLASK_DEBUG=1
```

Set on macOS/Linux:
```bash
export FLASK_DEBUG=1
```

## Project Structure

```
RecipeApp/
├── src/
│   ├── __init__.py          # Empty init file
│   ├── app.py                # Main Flask application
│   ├── models.py             # Database models
│   └── recipe_service.py     # TheMealDB API integration
├── instance/
│   └── recipes.db            # SQLite database (auto-created)
├── recipe-app-venv/          # Virtual environment
├── requirements.txt          # Python dependencies
├── Procfile                  # Deployment configuration
└── README.md                 # This file
```

## Usage

1. Navigate to `http://127.0.0.1:5000` in your browser
2. Enter an ingredient (e.g., "chicken breast", "beef", "salmon")
3. Click "Submit" to get a recipe suggestion
4. Your viewed recipes will appear in the history section

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Home page with search form |
| `/get_recipe` | POST | Search and display recipe by ingredient |
| `/history` | GET | View user's recipe history |
| `/recipes-by-ingredient/<ingredient>` | GET | View all recipes for an ingredient |

## Database Models

- **UserSession**: Tracks unique user sessions
- **Recipe**: Stores recipe details from TheMealDB
- **UserRecipe**: Links users to viewed recipes
- **Ingredient**: Stores unique ingredients
- **RecipeIngredient**: Many-to-many relationship between recipes and ingredients

## Deployment

The application includes a `Procfile` for Heroku deployment:

```
web: gunicorn "src.app:app" --bind 0.0.0.0:$PORT
```

## Dependencies

- Flask - Web framework
- Flask-SQLAlchemy - Database ORM
- requests - HTTP library for API calls
- gunicorn - WSGI HTTP server (production)

## License

MIT License
