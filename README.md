# Volunteer Connect Backend

## Overview
This repository contains the Flask REST API backend for Volunteer Connect, a full-stack web application that connects volunteers with organizations offering volunteer opportunities. The backend provides authentication, role-based access control, database persistence, and RESTful endpoints consumed by a React frontend.

The backend is designed to support real-world workflows such as volunteer applications, organization management, and payments, while maintaining a clean and scalable architecture.

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite (development) / PostgreSQL (production)
- RESTful API architecture

## Project Structure
# Volunteer Connect Backend

## Overview
This repository contains the Flask REST API backend for Volunteer Connect, a full-stack web application that connects volunteers with organizations offering volunteer opportunities. The backend provides authentication, role-based access control, database persistence, and RESTful endpoints consumed by a React frontend.

The backend is designed to support real-world workflows such as volunteer applications, organization management, and payments, while maintaining a clean and scalable architecture.

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite (development) / PostgreSQL (production)
- RESTful API architecture

# Volunteer Connect Backend

## Overview
This repository contains the Flask REST API backend for Volunteer Connect, a full-stack web application that connects volunteers with organizations offering volunteer opportunities. The backend provides authentication, role-based access control, database persistence, and RESTful endpoints consumed by a React frontend.

The backend is designed to support real-world workflows such as volunteer applications, organization management, and payments, while maintaining a clean and scalable architecture.

## Tech Stack
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Flask-Bcrypt
- SQLite (development) / PostgreSQL (production)
- RESTful API architecture

## Project Structure

## Database Models
The backend uses a relational database with the following core models:
- User
- Organization
- Opportunity
- Application
- Payment

## Relationships
- A user can own multiple organizations
- An organization can create multiple opportunities
- Users and opportunities have a many-to-many relationship through applications
- Applications include user-submitted attributes such as motivation messages
- Payments associate users with opportunities

## Authentication and Roles
Users register and authenticate as one of two roles:
- Volunteer
- Organization

Passwords are securely hashed, and role-based access controls determine which endpoints and resources a user can access.

## API Functionality

### Users
- Register a new user
- Login
- View user profile

### Organizations
- Create an organization
- View organization details
- Update organization
- Delete organization

### Opportunities
- Create an opportunity
- View all opportunities
- View a single opportunity
- Update an opportunity
- Delete an opportunity

### Applications
- Apply to an opportunity
- View applications
- Update application status

### Payments
- Create a payment record
- View payment history

## Setup Instructions

### Clone the Repository
```bash
git clone https://github.com/Httpednah/volunteer-connect-backend.git
cd volunteer-connect-backend
