
# College Placement Management System

A **Django-based web application** designed to streamline and manage the college placement process by connecting **students, companies, and administrators** on a single platform.

---

## 📌 Project Overview

The **College Placement Management System** automates placement-related activities such as job postings, student applications, training class management, and interview coordination.
It reduces manual effort, improves transparency, and ensures structured data handling for placement cells.

---

## 🎯 Objectives

* Digitize the college placement workflow
* Simplify job posting and application tracking
* Enable efficient training and class management
* Provide role-based access for Admin, Company, and Students

---

## 🧑‍💼 User Roles & Features

### 🔹 Admin

* Manage departments, courses, batches, locations, and class types
* Create and manage training classes
* View and manage companies and students
* Monitor placement activities

### 🔹 Company

* Register and manage company profile
* Post job openings
* View student applications
* Schedule interviews

### 🔹 Student

* Register and manage profile
* View available job opportunities
* Apply for jobs
* Track application status

---

## 🛠️ Technologies Used

* **Backend:** Django (Python)
* **Frontend:** HTML, CSS, Bootstrap, JavaScript, jQuery
* **Database:** SQLite3
* **AJAX:** For dynamic dropdowns and validations
* **Version Control:** Git & GitHub

---

## 📂 Project Structure

```
college-placement-system/
│
├── accounts/          # Authentication and user management
├── adminapp/          # Admin module
├── companyapp/        # Company module
├── guestapp/          # Guest & student module
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── manage.py
├── db.sqlite3
├── .gitignore
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/malavika-biju/college-placement-system.git
cd college-placement-system
```

### 2️⃣ Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate 
```

### 3️⃣ Install Dependencies

```bash
pip install django
```

### 4️⃣ Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5️⃣ Start the Server

```bash
python manage.py runserver
```

Open in browser:

```
http://127.0.0.1:8000/
```

---

## 🔐 Default Notes

* Database used: **SQLite3** (for development)
* `.env` and sensitive files are excluded using `.gitignore`
* Project follows **MVC architecture** (Django MVT)

---

## 📈 Future Enhancements

* Email notifications for job updates
* Resume upload and verification
* Role-based dashboards
* Advanced filtering and search
* Deployment on cloud platform

---

## 📄 License

This project is developed for **educational purposes**.
You are free to modify and extend it.

---

## 👩‍💻 Author

**Malavika Biju**
BCA Student
Django Developer (Beginner–Intermediate)

GitHub: [https://github.com/malavika-biju](https://github.com/malavika-biju)
