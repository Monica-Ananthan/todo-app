# Django To-Do App

A simple To-Do application built using Django with HTMX, Alpine.js, and Tailwind CSS.  
The application supports real-time updates without page reloads and is suitable for production deployment.

---

## Features

- Create tasks
- Edit tasks inline
- Update due dates
- Mark tasks as completed
- Delete tasks
- Real-time UI updates using HTMX
- Minimal frontend interactivity using Alpine.js
- Toast notifications for user actions(Task added, Category added, Title updated on edit, Date updated on edit, Task updated on check complete, Task delete )

---

## Tech Stack

- Backend: Django
- Frontend: HTML, Tailwind CSS
- Frontend Interactivity: HTMX, Alpine.js
- Database: PostgreSQL
- Deployment: Render

---

## Project Structure
todo-app/
│── todo_project/
│ ├── settings.py
│ ├── urls.py
│ ├── wsgi.py
│
│── todo_app/
│ ├── models.py
│ ├── views.py
│ ├── urls.py
│ ├── templates/
│
│── manage.py
│── requirements.txt


---

## Setup Instructions

### Clone the repository

```bash
git clone https://github.com/your-username/todo-app.git
cd todo-app
python -m venv venv
source venv\Scripts\activate

---

Install dependencies

pip install -r requirements.txt
python manage.py makemigrations #Run migrations
python manage.py migrate
python manage.py runserver #Run development server

http://127.0.0.1:8000/ #Local

https://todo-app-vh05.onrender.com/ #Production(Render)


Author
Monica Ananthan