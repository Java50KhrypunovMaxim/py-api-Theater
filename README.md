Theatre API

**Theatre API** is an API designed for managing theatrical performances, actors, theatre halls, and ticket reservations.

## Key Features:

1. **Genres** - Create and list genres.
2. **Actors** - Create and list actors.
3. **Theatre Halls** - Create and list theatre halls.
4. **Plays** - Create, update, and view plays.
5. **Performances** - Create, update, and view performances.
6. **Reservations** - Create and view reservations, manage tickets.

## Installation

### 1. Clone the Repository

First, clone the repository from GitHub:

```bash
git clone https://github.com/your_username/your-repository-name.git
cd your-repository-name
2. Install Dependencies
Make sure you have python and pip installed. To install dependencies, run:

pip install -r requirements.txt
3. Set Up Database
The project uses a PostgreSQL database. Create a database and set up the necessary configurations in the settings.py file under the DATABASES section. Ensure that the following environment variables are set: POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, and POSTGRES_PORT.

4. Run Migrations
Run the following command to apply database migrations and set up the necessary tables:

python manage.py migrate
5. Create a Superuser
To access the Django admin interface, create a superuser:

python manage.py createsuperuser
Follow the prompts to set up your superuser account.

6. Run the Project
Start the development server:

python manage.py runserver
Now the API will be accessible at: http://127.0.0.1:8000/.

Using the API

1. Authentication
To access most endpoints, authentication is required. You can use token-based authentication, which can be generated through the Django Admin or via the API.

2. Example Requests
Get the list of genres:
GET /genres/
Get the list of actors:
GET /actors/
Get the list of plays:
GET /plays/
3. Managing Reservations
Create a reservation:
POST /reservation/
Provide the ticket and performance information in the request body.

4. Request and Response Examples
For each endpoint, detailed request and response examples can be found through the Browsable API, which is available after starting the server.

Docker Usage (If applicable)

Build the Docker image:
docker build -t theatre-api .
Run the container with the database and API server:
docker-compose up
Now the application will be available on port 8000.

Documentation

API documentation is automatically generated using drf_spectacular and is available at:

http://127.0.0.1:8000/schema/
Project Structure

/theatre
    /migrations
    /models.py       # Data models
    /serializers.py  # Serializers
    /views.py        # Views
    /urls.py         # API routing
    /admin.py        # Admin interface
    /permissions.py  # Permissions
Database

The database uses PostgreSQL, and the tables are related via foreign keys. Here’s the database structure:

Genre: Stores the genres of plays.
Actor: Stores information about actors.
TheatreHall: Theatre halls with seating information.
Play: Contains information about plays, including actors and genres.
Performance: Represents the performances of plays in theatre halls.
Ticket: Stores information about tickets for performances.
Reservation: Stores booking details related to tickets.

