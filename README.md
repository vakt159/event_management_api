# Event Management API
A Django-based REST-Api that manages events (like conferences, meetups, etc.). The
application allows users to create, view, update, and delete events and register to events.
 
## Features

- User registration and JWT login
- CRUD operation for event
- Event registration endpoint for authenticated users
- Event filtering by date, title, description, and location
- API documentation via drf-spectacular and Swagger UI
- Celery task for sending registration email notifications
- Docker Compose setup for app, PostgreSQL, Redis, Celery, and MailHog

## API Endpoints

- `POST /api/users/register/` - register a new user
- `POST /api/users/login/` - obtain JWT token pair
- `POST /api/users/token/refresh/` - refresh access token
- `GET /api/event/` - list all events
- `POST /api/event/` - create a new event
- `GET /api/event/{id}/` - retrieve event details
- `PATCH /api/event/{id}/` - update an event (organizer only)
- `DELETE /api/event/{id}/` - delete an event (organizer only)
- `PATCH /api/event/{id}/register/` - register current user for the event
- `GET /api/schema/` - OpenAPI schema
- `GET /api/schema/swagger-ui/` - Swagger UI

## Run from GitHub

Clone the repository and start the app:

```sh
git clone https://github.com/vakt159/event_management_api
cd event_management_api
```

Then use Docker Compose:

```sh
docker-compose up --build
```
