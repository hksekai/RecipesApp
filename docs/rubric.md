# Project Rubric

This document outlines the grading criteria for the RecipeApp project.

## Grading Rubric

| Requirement | C Level | B Level | A Level | Current |
|-------------|:-------:|:-------:|:-------:|:-------:|
| **Web Application** - Basic form, reporting | ✅ | ✅ | ✅ | ✅ |
| **Data Collection** | ✅ | ✅ | ✅ | ✅ |
| **Data Analyzer** | ✅ | ✅ | ✅ | ✅ |
| **Unit Tests** | ✅ | ✅ | ✅ | ✅ |
| **Data Persistence** - Any data store | ✅ | ✅ | ✅ | ✅ |
| **REST Collaboration** - Internal or API endpoint | ✅ | ✅ | ✅ | ✅ |
| **Product Environment** | ✅ | ✅ | ✅ | ✅ |
| **Integration Tests** | ❌ | ✅ | ✅ | ✅ |
| **Using Mock Objects** (or any test doubles) | ❌ | ✅ | ✅ | ✅ |
| **Continuous Integration** | ❌ | ✅ | ✅ | ❌ |
| **Production Monitoring** - Instrumenting | ❌ | ❌ | ✅ | ❌ |
| **Event Collaboration** - Messaging | ❌ | ❌ | ✅ | ❌ |
| **Continuous Delivery** | ❌ | ❌ | ✅ | ❌ |

## Legend

- ✅ = Required / Completed
- ❌ = Not required / Not completed

## Current Status Notes

### ✅ Completed Requirements

1. **Web Application** (`src/app.py`)
   - Flask web application with HTML forms
   - Routes: `/` (home with search form), `/get_recipe` (POST), `/history`, `/recipes-by-ingredient/<ingredient>`
   - Basic reporting through recipe history views

2. **Data Collection** (`src/app.py`, `src/models.py`)
   - User input collection via web forms
   - Session tracking with unique user IDs
   - Recipe view history tracking

3. **Data Analyzer** (`src/recipe_service.py`)
   - RecipeService class fetches and processes recipe data from TheMealDB API
   - Analyzes ingredients to suggest recipes

4. **Unit Tests** (`test/recipe_service_tests.py`)
   - Unit tests implemented using `unittest` framework
   - Tests RecipeService functionality

5. **Data Persistence** (`src/models.py`, `instance/recipes.db`)
   - SQLite database with SQLAlchemy ORM
   - Models: UserSession, Recipe, UserRecipe, Ingredient, RecipeIngredient
   - Many-to-many relationships between recipes and ingredients

6. **REST Collaboration** (`src/recipe_service.py`, `src/app.py`)
   - External API integration with TheMealDB
   - Internal REST endpoints for recipe retrieval and history

7. **Product Environment** (`Procfile`, git remotes)
   - Deployed to Heroku: `https://git.heroku.com/pieong-recipe-app-d83c26a19785.git`
   - Procfile configured for Gunicorn

8. **Using Mock Objects** (`test/recipe_service_tests.py`)
   - Uses `unittest.mock.MagicMock` for mocking HTTP requests to TheMealDB API

9. **Integration Tests** (`test/app_integration_test.py`)
   - 4 integration tests implemented
   - Tests cover: recipe search success, no results, home page, and history tracking
   - Uses Flask test client with in-memory SQLite database
   - Mocks external API calls while testing full request/response cycle

### ❌ Not Completed Requirements

1. **Continuous Integration**
   - No `.github/workflows/` directory
   - No CI/CD configuration files (GitHub Actions, Travis CI, etc.)

2. **Production Monitoring**
   - No application performance monitoring (APM) tools detected
   - No logging framework beyond basic Flask logging
   - No health check endpoints

3. **Event Collaboration - Messaging**
   - No message broker (RabbitMQ, Kafka, AWS SQS, etc.)
   - No async task queues (Celery, etc.)
   - AI usage docs mention intent to use messaging but not implemented

4. **Continuous Delivery**
   - No automated deployment pipeline
   - Heroku deployment appears manual via git push

## Description of Requirements

### Core Requirements (All Levels)
- **Web Application**: Basic forms and reporting functionality
- **Data Collection**: Ability to collect and process data
- **Data Analyzer**: Tools for analyzing collected data
- **Unit Tests**: Automated testing of individual components
- **Data Persistence**: Storage solution (database, file system, etc.)
- **REST Collaboration**: RESTful API integration or endpoints
- **Product Environment**: Deployed to a production environment

### Intermediate Requirements (B & A Level)
- **Integration Tests**: Testing of integrated components
- **Using Mock Objects/Fakes/Spies**: Test doubles for isolated testing
- **Continuous Integration**: Automated build and test pipeline

### Advanced Requirements (A Level Only)
- **Production Monitoring**: Application performance monitoring and logging
- **Event Collaboration**: Messaging/queue systems for async communication
- **Continuous Delivery**: Automated deployment pipeline
