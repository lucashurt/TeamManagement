# PrjctMngr
### Collaborative Project Manager Web Application 
This web application was designed to provide a platform for individuals to create teams with others and manage projects with others through a team dashboard where all members can track the progress of all others through progress reports. This web application was built using Django to handle backend logic including hte databse models and API endpoints, while JavaScript was used to enable dynamic client-side interactions and DOM updates. In the application, admins can create tasks, edit members, edit tasks, archive projects, and view progress reports of all members. The project was designed to help teams be able to be kept updated on the progress of others for improved collaboration and coordination. In the future i hope to implement a real-time chat feature between teams using web-sockets to improve team communication past just progress reports.

### Features
* Authentification - Users can register,log in and out. This is handled using Django's built-on authentification system
* Team Management - Users can create teams, invite friends, manage team members and archive projects
* Task Management - Team admins can create and assign tasks with deadlines and descriptions for members
* Task Reporting - Members can report their task progress and percentage to admins and other members in the dashboard
* Friends - Users can search other users and send friend requests, the user can then accept or reject these friend requests
* CSRF Protection - Every single JS Fetch request or API call has CSRF certification to ensure security for users

### Installating and Running Project
Run the following in the command line exluding the bulletpoint numbers
1. python3 -m venv myenv
2. source myenv/bin/activate
3. pip install Django
4. python manage.py runserver

### Main Files Created
* views.py: Contains all the view functions responsible for handling user interactions and rendering templates.
* models.py: Defines the database schema, including models for User, Team, Task, and FriendRequest.
* urls.py: Maps URLs to their corresponding view functions.
* templates/: Contains the HTML templates for rendering pages such as the index, login, profile, and team views.
* static/: Includes the static JavaScript files and images used in the app for styling and client-side functionality.
* requirements.txt: Lists all the Python dependencies required to run the project.
* README.md: This file, providing an overview of the project.
  
