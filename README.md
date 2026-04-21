## Overview
Eating well comes with challenges for students, who often have no reliable way to know if the food options fits their needs or whether the line is even worth it… Imagine a single app that allows students to find food on and around campus and that’s easy, reliable, and as simple as opening your phone.

HungryHusky is a unified app with the purpose of improving the dining experience for students. It is a platform that allows discovery, reviewing, and tracking of food options on and around campus ranging from campus dining halls to nearby restaurants.

School is hard, eating shouldn't have to be.

## Key Features
HungryHusky is tailored to support two user groups:

- **Students**: View restaurants, dining halls, and menu items, view and update wait times and reviews.
   - Alex, a freshman with allergies, wants to be able to see what items are available at dining halls and submit feedback for a dining hall. He also wishes to create an allergen profile for himself.
   - Ryan, a senior foodie, wishes to be able to view and filter restaurants near him, as well as check wait times and save spots to his to-try list.
- **Admins**: View student feedback, update dining hall details, and review overall student experience.
   -Mary, a dining services manager, wishes to update dining hall hours quickly, as well as view student preferences and feedback.
   -Dr. Garcia, the director of campus food services, values gaining insights into student feedback as well as dining hall usage stats.

## Technology Stack
The project follows a three-tier architecture approach running on Docker containers.

The three components that run in their own Docker containers:
- Backend: Python Flask REST API for data access and business logic. Runs in the ./api directory.
- Database: MySQL for storage of data information including restaurants, dining halls, users, and admins. Runs in the ./database-files directory.
- Frontend: Streamlit user interface for an immersive, dynamic experience. Runs in the ./app directory.

## Project Setup
### Prerequisites
Ensure that you have the following installed on your computer:
- Docker
- MySQL
- Python

1. Create an .env file in the root directory. You can use the template in .env.template. Update the values accordingly.
2. For running the testing containers:
      i. docker compose up -d to start all the containers in the background
      ii. docker compose down to shutdown and delete the containers
      iii. docker compose up db -d only start the database container (replace db with api or app for the other two services as needed)
      iv. docker compose stop to "turn off" the containers but not delete them.
4. Access the link provided (in Docker) after running the previous command to see the Streamlit page. You should be able to navigate the user stories from here.
5. To restart the container if there are any changes with any SQL files: 
      i. From the root directory, run docker compose down db -v && docker compose up db -d
