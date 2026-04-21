## Key Features

### HungryHusky is tailoerd to support two user groups:
- students: View restaurants, dining halls, and menu items, view and update wait times and reviews.
- admins: View student feedback, update dining hall details, and review overall student experience.

## Technology Stack
The project follows a three-tier architecture approach running on Docker containers.

- Backend: Python Flask REST API for data access and business logic. Runs in the ./api directory.
- Database: MYSQL for storage of data information including restaurants, dining halls, users, and admins. Runs in the ./database-files directory.
- Frontend: Streamlit user interface for an immersive, dynamic experience. Runs in the ./app directory.

## Project Setup
### Prerequisites
Ensure that you have the following installed on your computer:
- Docker
- MySQL
- Python

1. Create an .env file in the root directory. You can use the template in .env.template. Update the values accordingly.
2. From the root directory, run docker-compose down.
3. From the root directory, run docker-compose up --build. This will build the frontend and backend containers, create the database, and run all services together.
4. Access the link provdied after running the previous command to see the Streamlit page. You should be able to navigate the user stories from here.
5. To restart the container if there are any changers with Docker, run steps 2 and 3 again.