# Employee Management System

A Django-based employee management system with role-based access control, featuring department management, employee records, attendance tracking, and performance records.

## Features

- **Role-based Authentication**: Admin, HR, and Employee roles with different permission levels
- **Department Management**: Create, view, update, and delete departments
- **Employee Management**: Maintain employee details with department assignments
- **Attendance Tracking**: Record and monitor employee attendance (present, late, absent)
- **Performance Assessment**: Track employee performance evaluations
- **Dashboard**: Interactive visual dashboard with department distribution and attendance statistics
- **API Documentation**: Swagger and ReDoc API documentation

## Technology Stack

- **Backend**: Django 5.1, Django REST Framework
- **Authentication**: JWT (JSON Web Tokens)
- **Database**: PostgreSQL
- **Frontend**: HTML, CSS, JavaScript, Chart.js
- **Documentation**: drf-yasg (Swagger/ReDoc)

## Installation

### Prerequisites

- Python 3.8+
- PostgreSQL

### Setup

1. **Clone the repository**

 ```bash
   git clone https://github.com/yourusername/employee-management.git
   cd employee-management
```
2. **Create and activate a virtual environment**
3. **Install dependencies**
4. **Configure the database**
   Create a `.env` file in the root directory of the project with the following content:
```
DATABASE_URL= your-database-url
SECRET_KEY=your-secret-key-here
```
5. **Apply migrations**
6. **Create a superuser**
7. **Seed the database with test data (optional)**
8. **Run the development server**


## API Endpoints

### Authentication:
- `POST /api/token/`: Obtain JWT token
- `POST /api/token/refresh/`: Refresh JWT token

### User Management:
- `GET /api/accounts/users/`: List users (Admin/HR only)
- `POST /api/accounts/register/`: Register new user

### Departments:
- `GET /api/departments/`: List departments
- `POST /api/departments/`: Create department (HR/Admin only)
- `GET /api/departments/{id}/`: Retrieve department
- `PUT /api/departments/{id}/`: Update department (HR/Admin only)
- `DELETE /api/departments/{id}/`: Delete department (HR/Admin only)

### Employees:
- `GET /api/employees/`: List employees (HR/Admin see all, Employees see own)
- `POST /api/employees/`: Create employee (HR/Admin only)
- `GET /api/employees/{id}/`: Retrieve employee details
- `PUT /api/employees/{id}/`: Update employee (HR/Admin only)
- `DELETE /api/employees/{id}/`: Delete employee (HR/Admin only)

### Attendance:
- `GET /api/attendance/`: List attendance records
- `POST /api/attendance/`: Create attendance record (HR/Admin only)
- `GET /api/attendance/{id}/`: Retrieve attendance record
- `PUT /api/attendance/{id}/`: Update attendance record (HR/Admin only)
- `DELETE /api/attendance/{id}/`: Delete attendance record (HR/Admin only)

### Performance:
- `GET /api/performance/`: List performance records
- `POST /api/performance/`: Create performance record (HR/Admin only)
- `GET /api/performance/{id}/`: Retrieve performance record
- `PUT /api/performance/{id}/`: Update performance record (HR/Admin only)
- `DELETE /api/performance/{id}/`: Delete performance record (HR/Admin only)

## Role Permissions

* **Admin**: Full access to all features and data
* **HR**: Can manage departments, employees, attendance, and performance, but cannot manage users
* **Employee**: Can view own data and all departments, but cannot modify any data

## Project Structure
```
djangoAssessment/
├── accounts/            # User authentication and role management
├── dashboard/           # Main dashboard and visualization
├── department/          # Department management
├── employee/            # Employee management
├── attendance/          # Attendance tracking
├── performance/         # Performance assessment
├── djangoAssessment/    # Main project settings
└── static/              # Static files (CSS, JS)
```
