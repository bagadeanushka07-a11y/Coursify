# 🎓 Coursify

Coursify is a Django-based e-learning platform designed to provide a complete online learning experience for students and instructors.

The platform supports course management, lessons, quizzes, student enrollment, progress tracking, certificates, reviews, instructor analytics, and role-based dashboards.

---

## 🚀 Features

### 👨‍🎓 Student Features

- Student registration and login
- Student dashboard
- Browse and explore courses
- Enroll in courses
- View enrolled courses
- Access course lessons
- Track lesson progress
- Take quizzes
- View quiz results
- View quiz performance
- Course completion tracking
- Earn certificates
- View certificates
- Course reviews and ratings
- Profile management
- Account settings

---

### 👨‍🏫 Instructor Features

- Instructor dashboard
- Create courses
- Edit courses
- Delete courses
- Manage course lessons
- Create and manage quizzes
- Add quiz questions
- Monitor quiz attempts
- Track student performance
- View course analytics
- View quiz analytics
- View student progress
- Track course completion
- Monitor enrollment statistics
- Instructor analytics dashboard

---

### 🛡️ Admin Features

- Role-based access
- Course management
- Quiz management
- User management through Django administration
- Platform administration

---

## 📊 Analytics

Coursify includes an instructor analytics system that provides information such as:

- Total courses
- Total students
- Total lessons
- Course completion rate
- Total quizzes
- Quiz attempts
- Quiz students
- Average quiz score
- Average quiz percentage
- Passed attempts
- Quiz pass rate
- Course performance
- Student performance
- Lesson progress
- Course progress

---

## 📝 Quiz System

The quiz system allows instructors to create quizzes for their courses.

Students can:

- Attempt quizzes
- Submit answers
- View scores
- View percentages
- Track quiz performance

Instructors can:

- Create quizzes
- Add questions
- Manage quizzes
- Monitor attempts
- View average scores
- View pass rates
- Analyze student quiz performance

---

## 🎓 Certificate System

Students can receive certificates after completing eligible courses.

The certificate system includes:

- Certificate generation
- Certificate listing
- Certificate detail page
- Course completion verification

---

## 🏗️ Project Structure

```text
Coursify/
│
├── accounts/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── categories/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   └── views.py
│
├── certificates/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── courses/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── dashboard/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── enrollments/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── lessons/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── quizzes/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── reviews/
│   ├── migrations/
│   ├── admin.py
│   ├── models.py
│   └── views.py
│
├── user_settings/
│   ├── migrations/
│   ├── admin.py
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
│
├── templates/
│   ├── accounts/
│   ├── certificates/
│   ├── courses/
│   ├── dashboard/
│   ├── enrollments/
│   ├── lessons/
│   ├── quizzes/
│   └── user_settings/
│
├── manage.py
├── .gitignore
└── README.md

🛠️ Technologies Used
Python
Django
HTML5
CSS3
JavaScript
SQLite
Django Templates
Django ORM
Django Authentication
Git
GitHub
🔐 User Roles

Coursify uses role-based access control.

Student

Students can:

Browse courses
Enroll in courses
Study lessons
Complete lessons
Attempt quizzes
Track progress
Earn certificates
Instructor

Instructors can:

Create courses
Manage lessons
Create quizzes
Monitor students
View analytics
Track course performance
Admin

Administrators can manage the platform through administrative functionality and Django Admin.

💻 Installation
1. Clone the repository
git clone https://github.com/bagadeanushka07-a11y/Coursify.git
2. Navigate to the project
cd Coursify
3. Create a virtual environment

Windows:

python -m venv venv

Activate it:

venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate
4. Install dependencies
pip install django

If a requirements.txt file is added to the project later, use:

pip install -r requirements.txt
5. Apply migrations
python manage.py migrate
6. Create an admin account
python manage.py createsuperuser

Follow the prompts to create the administrator account.

7. Start the development server
python manage.py runserver

The application will be available at:

http://127.0.0.1:8000/
👤 Demo Accounts

For security reasons, real passwords are not stored in this README.

Use demo/test accounts created specifically for development.

Example:

Role	Username	Password
Instructor	instructor_demo	YOUR_DEMO_PASSWORD
Student	student_demo	YOUR_DEMO_PASSWORD

⚠️ Never commit real passwords, API keys, secret keys, database credentials, or other sensitive information to a public repository.

🔒 Security

This project is intended for development and portfolio purposes.

Before deploying to production:

Change the Django SECRET_KEY
Set DEBUG = False
Configure ALLOWED_HOSTS
Use environment variables for secrets
Use a production database
Configure HTTPS
Secure authentication credentials
Configure static and media files
Review permissions and role-based access
Never commit real user passwords
Never commit production credentials
📱 Responsive Design

The frontend is designed to work across different screen sizes, including:

Desktop
Laptop
Tablet
Mobile devices

The dashboard includes responsive navigation and a mobile sidebar menu.

📈 Instructor Analytics

The instructor analytics dashboard provides detailed insights into teaching performance.

It includes:
Course Statistics
       ↓
Student Statistics
       ↓
Lesson Statistics
       ↓
Quiz Statistics
       ↓
Course Performance
       ↓
Quiz Performance
       ↓
Student Performance
his allows instructors to understand how students are progressing through their courses.

🗃️ Main Django Applications
Application	Purpose
accounts	Authentication and user accounts
categories	Course categories
certificates	Student certificates
courses	Course management
dashboard	User dashboards
enrollments	Course enrollment
lessons	Course lessons and progress
quizzes	Quizzes, questions and attempts
reviews	Course reviews
user_settings	User settings
🔄 Application Flow

User Registration
       ↓
    Login
       ↓
   Dashboard
       ↓
 ┌───────────────┐
 │               │
Student       Instructor
 │               │
 ↓               ↓
Explore        Create Course
Courses           ↓
 │             Add Lessons
 ↓                 ↓
Enroll          Create Quiz
 │                 ↓
 ↓             View Analytics
Study
 │
 ↓
Complete Lessons
 │
 ↓
Take Quizzes
 │
 ↓
Complete Course
 │
 ↓
Earn Certificate
🧪 Development

Run Django's system checks:

python manage.py check

Create migrations after model changes:

python manage.py makemigrations

Apply migrations:

python manage.py migrate

Run the development server:

python manage.py runserver
🌐 Repository

GitHub:

https://github.com/bagadeanushka07-a11y/Coursify

👩‍💻 Author

Anushka Bagade

Coursify was developed as a Django e-learning platform project demonstrating:

Backend development
Database design
Authentication
Role-based authorization
CRUD operations
Course management
Quiz systems
Student progress tracking
Analytics
Responsive frontend development
