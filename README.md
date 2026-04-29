# 🦺 epi-detection-django
Web platform for EPI detection built with Django and YOLOv8.

## ⚙️ Software Versions
- Python 3.12
- YOLOv8

## 🚀 Installation
### 1. Clone Repository
```
git clone https://github.com/epidetectapp/django-mvt.git
```
### 2. Set Up Virtual Environment (Recommended)

#### 2.1 Create Virtual Environment
```
py -3.12 -m venv .venv
```
#### 2.2 Activate Virtual Environment
```
.\.venv\Scripts\activate
```
### 3. Install Requirements
```
pip install -r requirements.txt
```

### 4. Run Database Migrations
```
python manage.py migrate
```

## 👤 Create Superuser (Recommended)
### 1. Run Command
```
python manage.py createsuperuser
```
### 2. Example Credentials
- Email: joao@gmail.com
- Nome: João
- Sobrenome: Pereira 
- Telefone: (99) 01234-5678    
- Password: admin123
### 3. Access Admin Panel
```
http://127.0.0.1:8000/admin/
```
## ▶️ Run Application
### 1. Start Local Server
```
python manage.py runserver
```

### 2. Open in Browser
```
http://127.0.0.1:8000/
```

## 🎥 Demonstration
https://github.com/user-attachments/assets/a79e1ef6-4d54-40f4-ae90-114e57b620c3