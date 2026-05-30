# 🏡 Homestay Booking Platform

> A full-stack DevSecOps capstone project — secure homestay booking web application deployed on AWS infrastructure.

![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20VPC%20%7C%20ALB%20%7C%20CloudWatch-orange?style=flat-square&logo=amazon-aws)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-3.x-black?style=flat-square&logo=flask)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-green?style=flat-square&logo=nginx)
![GitHub Actions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-blue?style=flat-square&logo=github-actions)

---

## 📌 Project Overview

**Homestay** is a production-grade booking platform for Kerala homestay properties, built as part of the **IPSR Solutions FYUGP Summer Internship 2026** — DevSecOps Foundations for Cloud & AWS track.

The project demonstrates end-to-end DevSecOps practices including secure AWS infrastructure, a Python/Flask REST API, JWT-based authentication, CI/CD automation, and CloudWatch monitoring.

**Live URL:**
```
http://homestay-alb-1661767430.ap-south-1.elb.amazonaws.com
```

---

## 🏗️ Architecture

```
Internet
    │
    ▼
[Application Load Balancer]
    │
    ▼
┌─────────────────────────────────────────────┐
│           homestay-vpc (10.0.0.0/16)        │
│                                             │
│  Public Subnet (10.0.7.0/24)               │
│  ┌───────────────────────┐                 │
│  │   Bastion Host        │                 │
│  │   homestay_bastion    │                 │
│  │   t3.micro / Ubuntu   │                 │
│  └───────────────────────┘                 │
│            │ SSH Jump                       │
│            ▼                               │
│  Private Subnet (10.0.128.0/20)            │
│  ┌───────────────────────┐                 │
│  │   App Server          │                 │
│  │   homestay_app        │                 │
│  │   Flask + Gunicorn    │                 │
│  │   Nginx Reverse Proxy │                 │
│  └───────────────────────┘                 │
│            │                               │
│  ┌─────────▼──────────┐                   │
│  │   NAT Gateway       │                   │
│  └────────────────────┘                   │
└─────────────────────────────────────────────┘
         │
         ▼
[CloudWatch Monitoring] [SNS Alerts] [S3 Backups]
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3.11, Flask, Gunicorn |
| **Database** | SQLite (SQLAlchemy ORM) |
| **Web Server** | Nginx (reverse proxy) |
| **Auth** | JWT (PyJWT), bcrypt |
| **Cloud** | AWS EC2, VPC, ALB, CloudWatch, SNS |
| **CI/CD** | GitHub Actions |
| **Security** | Fail2ban, UFW, SSH hardening |
| **OS** | Ubuntu 24.04 LTS |

---

## ✨ Features

### User Features
- 📝 Register and login with secure JWT authentication
- 🏡 Browse all available homestay properties
- 📅 Book properties with date selection and price calculator
- 📋 View personal booking history with status

### Admin Features
- ➕ Add new properties
- ✏️ Edit existing property details and pricing
- 🗑️ Delete properties
- 👥 View all registered users and manage roles
- 📊 Dashboard with total stats (users, properties, bookings)
- 📋 View all bookings with user email, property name, and total price

### Security Features
- 🔐 bcrypt password hashing (12 rounds)
- 🎫 JWT token authentication (HS256)
- 🛡️ SQL injection prevention via SQLAlchemy ORM
- 🚫 XSS prevention via Jinja2 auto-escaping
- 🔒 Security headers (X-Frame-Options, CSP, HSTS)
- ⏱️ Nginx rate limiting (10 req/s API, 5 req/min login)
- 🚧 Fail2ban brute-force protection
- 🔥 UFW firewall (ports 22, 80, 443 only)
- 🔑 SSH key-based auth, root login disabled
- 🏰 Bastion host as jump server

---

## 📁 Project Structure

```
homestay/
├── app.py                  # Flask application entry point
├── config.py               # App configuration
├── models.py               # SQLAlchemy database models
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container definition
├── README.md
├── .gitignore
├── routes/
│   ├── __init__.py
│   ├── auth.py             # Register, login, logout
│   ├── properties.py       # Property CRUD + JWT decorator
│   ├── bookings.py         # Booking creation and retrieval
│   └── admin.py            # Admin dashboard endpoints
├── templates/
│   ├── base.html           # Base layout with navbar and modals
│   ├── index.html          # Homepage with featured properties
│   ├── properties.html     # All properties listing
│   ├── booking.html        # Booking form and history
│   └── admin.html          # Admin dashboard
├── static/                 # CSS, JS, images
├── scripts/
│   └── backup.py           # Automated S3 backup script
├── docs/
│   ├── security.md         # Security controls documentation
│   └── deployment.md       # Full deployment guide
└── .github/
    └── workflows/
        └── deploy.yml      # CI/CD pipeline
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| POST | `/api/register` | None | Register new user |
| POST | `/api/login` | None | Login, returns JWT token |
| POST | `/api/logout` | JWT | Logout |

### Properties
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/properties` | None | List all properties |
| POST | `/api/properties` | JWT | Add new property |
| DELETE | `/api/properties/<id>` | JWT | Delete property |

### Bookings
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/bookings` | JWT | Get my bookings |
| POST | `/api/bookings` | JWT | Create booking |

### Admin
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| GET | `/api/admin/stats` | Admin | Dashboard stats |
| GET | `/api/admin/users` | Admin | All users |
| PUT | `/api/admin/users/<id>/role` | Admin | Update user role |
| GET | `/api/admin/properties` | Admin | All properties |
| POST | `/api/admin/properties` | Admin | Add property |
| PUT | `/api/admin/properties/<id>` | Admin | Edit property |
| DELETE | `/api/admin/properties/<id>` | Admin | Delete property |
| GET | `/api/admin/bookings` | Admin | All bookings |

---

## 🚀 Quick Start

### Prerequisites
- AWS Account
- EC2 Key Pair (`.pem` file)
- Python 3.11+
- Git

### Local Development

```bash
# Clone the repository
git clone https://github.com/adarshashokan/homestay.git
cd homestay

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your values

# Run the app
python3 app.py
# or
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Environment Variables

```env
SECRET_KEY=your-flask-secret-key
JWT_SECRET=your-jwt-secret-key
DATABASE_URL=sqlite:///homestay.db
S3_BUCKET=your-s3-bucket-name
AWS_REGION=ap-south-1
```

---

## ☁️ AWS Deployment

### Infrastructure
```
VPC CIDR:        10.0.0.0/16
Public Subnet:   10.0.7.0/24   (Bastion)
Private Subnet:  10.0.128.0/20 (App Server)
Region:          ap-south-1 (Mumbai)
```

### SSH Access
```bash
# From Windows - copy key to bastion
scp -i home.pem home.pem ubuntu@43.204.29.182:~/home.pem

# Connect to bastion
ssh -i home.pem ubuntu@43.204.29.182

# Jump to app server
ssh -i ~/home.pem ubuntu@10.0.140.5
```

---

## 🔄 CI/CD Pipeline

GitHub Actions automatically deploys on every push to `main`:

```
Push to main
    ↓
Lint with flake8
    ↓
SSH to Bastion
    ↓
SSH to App EC2
    ↓
git pull origin main
    ↓
pip install -r requirements.txt
    ↓
sudo systemctl restart homestay
    ↓
✅ Deployed
```

### Required GitHub Secrets
| Secret | Value |
|---|---|
| `BASTION_HOST` | `43.204.29.182` |
| `SSH_PRIVATE_KEY` | Contents of `home.pem` |

---

## 📊 Monitoring

### CloudWatch Metrics
| Metric | Threshold | Alarm |
|---|---|---|
| CPU Utilization | > 80% | `homestay-cpu-high` |
| Memory Usage | > 80% | `homestay-memory-high` |
| Disk Usage | > 85% | `homestay-disk-high` |
| Failed SSH Attempts | > 10 in 5min | `homestay-ssh-brute-force` |

### Log Groups
| Group | Source |
|---|---|
| `homestay-nginx-access` | Nginx access logs |
| `homestay-nginx-error` | Nginx error logs |
| `homestay-auth-logs` | SSH auth logs |

### Alerts
- SNS Topic: `homestay-alerts`
- Delivery: Email notification

---

## 🔐 Security Controls

| Control | Implementation |
|---|---|
| Password Hashing | bcrypt (12 rounds) |
| Authentication | JWT HS256 tokens |
| SQL Injection | SQLAlchemy ORM |
| XSS | Jinja2 auto-escaping |
| CSRF | Stateless JWT |
| Clickjacking | X-Frame-Options: DENY |
| Brute Force | Fail2ban + rate limiting |
| Transport | HTTPS via ALB |
| Firewall | UFW + Security Groups |
| Access Control | RBAC (user/admin roles) |

---

## 👨‍💻 Author

**Adarsh Ashokan**
FYUGP Summer Internship Program
IPSR Solutions · DevSecOps Foundations for Cloud & AWS · 2026

---

## 📄 License

This project is built for educational purposes as part of the IPSR Solutions internship program.

---

*Built with ❤️ in Kerala · Powered by AWS · Secured by DevSecOps*
