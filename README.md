# Fullstack Developer Capstone Project

This repository contains the backend and frontend code for the Fullstack Developer Capstone Project. Below are the instructions to set up, run, and manage this project.

## Table of Contents

- [Backend (Django)](#backend-django)
- [Frontend (React)](#frontend-react)
- [Docker Setup](#docker-setup)
- [IBM Cloud Deployment](#ibm-cloud-deployment)

---

## Backend (Django)

### 1. Set up Virtual Environment and Install Dependencies
```bash
cd /home/project/fullstack-developer-capstone/server
pip install virtualenv
virtualenv djangoenv
source djangoenv/bin/activate
python3 -m pip install -U -r requirements.txt

```

### 2. Database Migrations
```bash
python3 manage.py makemigrations
python3 manage.py migrate

```

### 3. Run the Django Server
```bash
python3 manage.py runserver

```

### 4. Build and Run the Node App with Docker (for database run)

```bash
cd /home/project/fullstack-developer-capstone/server/database
docker build . -t nodeapp
docker-compose up
```

### Frontend (React)
### 5. Install Dependencies and Build Frontend

```bash
cd /home/project/fullstack-developer-capstone/server/frontend
npm install
npm run build

```

### IBM Cloud Deployment
### 6. Build, Push, and Deploy Microservice on IBM Cloud

```bash
cd /home/project/fullstack-developer-capstone/server/djangoapp/microservices
docker build . -t us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
docker push us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer
ibmcloud ce application create --name sentianalyzer --image us.icr.io/${SN_ICR_NAMESPACE}/senti_analyzer --registry-secret icr-secret --port 5000

```



   

