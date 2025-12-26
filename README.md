
# 🎓 EduCore LMS API

![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-6.0-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/Django_REST-Framework-red?style=for-the-badge&logo=django&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Auth-000000?style=for-the-badge&logo=json-web-tokens&logoColor=white)

> **Enterprise-grade Learning Management System (LMS) Backend** built with Django REST Framework. Features Role-Based Access Control (RBAC), atomic nested writes, and high-performance query optimization.

## 🚀 Key Features

* 🔐 **JWT Authentication & RBAC**: Secure `Access` and `Refresh` token rotation. Custom permissions ensure **Students** can only view purchased content, while **Instructors** manage their own courses.
* ⚡ **Database Optimization**: Solved the N+1 query problem using `select_related`, `prefetch_related`, and database-level `Count()` annotations.
* 🧱 **Atomic Nested Writes**: Custom `create()` method in Serializers handles complex JSON payloads (Course -> Modules -> Lessons) in a single **ACID transaction**.
* 🛡️ **Production Security**: Implemented **Rate Limiting (Throttling)** to prevent DDoS attacks (10 req/min for users, 2/min for guests).
* 📚 **Self-Documenting**: Integrated **Swagger/OpenAPI** (`drf-spectacular`) for interactive API testing.
* 🔄 **API Versioning**: URLPathVersioning (`/api/v1/`) to ensure backward compatibility.

## 🛠️ Tech Stack

* **Framework:** Django 6.0, Django REST Framework
* **Auth:** SimpleJWT (Stateless Authentication)
* **Database:** SQLite (Dev) / PostgreSQL (Prod)
* **Documentation:** Drf-Spectacular (Swagger UI)
* **Utilities:** Django-Filter, Cors-Headers

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/token/` | Obtain Access/Refresh Tokens | ❌ |
| `GET` | `/api/v1/courses/` | List all courses (Pagination + Filtering) | ✅ |
| `POST` | `/api/v1/courses/` | Create Course with Nested Modules | ✅ (Instructor) |
| `GET` | `/api/v1/docs/` | Interactive Swagger UI | ❌ |

## 🏁 Quick Start

### 1. Clone the Repository
git clone [https://github.com/YOUR_USERNAME/educore-api.git](https://github.com/YOUR_USERNAME/educore-api.git)
cd educore-api

### 2. Setup Environment

python -m venv venv
# Windows
venv\Scripts\activate
# Mac/Linux
source venv/bin/activate

### 3. Install Dependencies

pip install -r requirements.txt

### 4. Run Migrations & Server

python manage.py migrate
python manage.py runserver

### 5. Access the API

Open your browser to: `http://127.0.0.1:8000/api/v1/docs/`

## 🧪 Testing

Run the automated test suite to verify permissions and validation rules:

python manage.py test courses

*Built with ❤️ by Dhruvit Patel*
