# DevOps Portfolio — Flask, Redis, Nginx & Docker

A small personal DevOps portfolio application I built to get hands-on experience with Docker, Docker Compose, networking, reverse proxies, persistent storage, and running multiple services together.

Instead of building just a static portfolio, I wanted the application itself to demonstrate some of the DevOps concepts I'm learning.

The application uses **Flask** for the web application, **Redis** for storing the visitor count, **Nginx** as a reverse proxy, and **Docker Compose** to run everything together.

---

## 📸 Application Preview

> Screenshots of the application will be added here.

<img width="1440" height="900" alt="Screenshot 2026-09-24 at 05 19 19" src="https://github.com/user-attachments/assets/399cba64-7350-4d01-ac5f-22bbce6c6d07" />

<img width="1440" height="900" alt="Screenshot 2026-09-24 at 05 19 39" src="https://github.com/user-attachments/assets/df77ef1c-7405-478b-8391-cfeceed9223d" />

<img width="1440" height="900" alt="Screenshot 2026-09-24 at 05 19 52" src="https://github.com/user-attachments/assets/18cfebfb-0d2c-4104-9213-4a8c9c956e75" />


---

##  What This Project Does

The application is a simple personal DevOps portfolio website.

It includes:

* Personal introduction and DevOps-focused portfolio
* GitHub profile button
* Technology overview
* DevOps skills section
* Application architecture explanation
* Redis-powered visitor counter
* Flask health-check endpoint
* Nginx reverse proxy
* Docker Compose multi-container setup
* Persistent Redis storage using a Docker volume

I wanted to keep the website itself simple and use the infrastructure behind it to demonstrate what I've been learning.

---

##  Architecture

The application consists of three main containers:

```text
                    Browser
                       |
                       | HTTP :5002
                       v
                +--------------+
                |    Nginx     |
                | Reverse Proxy|
                +------+-------+
                       |
                       | Docker Network
                       v
                +--------------+
                |    Flask     |
                |  Web App     |
                +------+-------+
                       |
                       | Redis
                       v
                +--------------+
                |    Redis     |
                | Visit Counter|
                +------+-------+
                       |
                       v
                +--------------+
                | Docker       |
                | Volume       |
                +--------------+
```

### Request Flow

When a user visits the website:

1. The browser sends a request to Nginx.
2. Nginx receives the request on port `5002`.
3. Nginx forwards the request to the Flask container.
4. Flask processes the request.
5. Flask communicates with Redis.
6. Redis increments the visitor count.
7. Flask passes the visitor count to the HTML template.
8. The page is returned to the browser.

---

## 🧰 Technologies Used

| Technology     | Purpose                              |
| -------------- | ------------------------------------ |
| Python         | Application programming language     |
| Flask          | Web application framework            |
| Redis          | Stores the visitor count             |
| Nginx          | Reverse proxy                        |
| Docker         | Containerisation                     |
| Docker Compose | Runs and manages multiple containers |
| Docker Volumes | Persistent Redis storage             |
| Git            | Version control                      |
| GitHub         | Source code hosting                  |

---

## 🐍 Flask

Flask is responsible for the web application and application logic.

The application has three main routes:

### `/`

Displays the portfolio website.

Every time the homepage is loaded, Flask increments the Redis visitor counter.

### `/count`

Increments and displays the visit count.

### `/health`

Checks whether Flask can communicate with Redis.

A successful response looks like:

```json
{
  "status": "healthy",
  "redis": "connected"
}
```

The health endpoint was added to help me understand how applications can expose a simple endpoint that infrastructure or monitoring systems can use to check application health.

---

## 🔴 Redis

Redis is used as a lightweight data store for the visitor counter.

When the homepage is loaded, Flask runs:

```python
visits = redis_count.incr("portfolio_visits")
```

Redis increments the value every time the page is visited.

For example:

```text
First visit   -> 1
Second visit  -> 2
Third visit   -> 3
Fourth visit  -> 4
```

The important part is that the count isn't stored inside Flask itself.

Flask communicates with Redis and Redis stores the value.

---

## 💾 Redis Persistence with Docker Volumes

Redis uses a Docker volume:

```yaml
volumes:
  - redis-data:/data
```

The volume provides persistent storage for Redis data.

The basic idea is:

```text
Redis Container
      |
      v
    /data
      |
      v
redis-data volume
```

This is useful because containers are replaceable.

For example:

```bash
docker compose down
```

removes the containers but doesn't remove the named Redis volume.

When the application is started again:

```bash
docker compose up
```

Redis can use the existing volume and retain its stored data.

If the volume is deliberately removed with:

```bash
docker compose down -v
```

the Redis data will also be removed.

This helped me understand the difference between **container lifecycle** and **persistent application data**.

---

## 🌐 Nginx

Nginx is used as a reverse proxy in front of Flask.

Instead of the browser communicating directly with Flask:

```text
Browser → Flask
```

the application uses:

```text
Browser → Nginx → Flask
```

The Nginx configuration contains:

```nginx
upstream flask_app {
    server web:5002;
}
```

and:

```nginx
location / {
    proxy_pass http://flask_app;
}
```

The Flask service is called `web` in Docker Compose.

Docker Compose provides internal DNS, which means Nginx can communicate with Flask using:

```text
web:5002
```

rather than relying on a hard-coded container IP address.

---

## 🔗 Docker Networking

One of the concepts I learned from this project was how containers communicate with each other.

Inside the Flask container, Redis isn't accessed using:

```text
localhost
```

because `localhost` would refer to the Flask container itself.

Instead, the application uses:

```text
REDIS_HOST=redis
```

`redis` is the name of the Redis service in `docker-compose.yml`.

Docker Compose creates a network that allows the services to communicate using their service names.

The internal communication therefore looks like:

```text
Nginx → web:5002

Flask → redis:6379
```

This was one of the concepts I found particularly useful because it helped me understand Docker networking rather than simply configuring containers without knowing how they communicate.

---

## 🐳 Docker Compose

Docker Compose is used to define the three services:

```yaml
services:
  web:
  redis:
  nginx:
```

This allows the entire application stack to be started with:

```bash
docker compose up
```

Instead of manually starting each container individually.

The Flask service is built from the project's Dockerfile:

```yaml
web:
  build:
    context: .
    dockerfile: Dockerfile
```

The Redis service uses the official Redis Alpine image:

```yaml
redis:
  image: redis:7-alpine
```

Nginx uses the official Nginx image:

```yaml
nginx:
  image: nginx:latest
```

---

## 📦 Dockerfile

The Flask application uses a multi-stage Docker build.

The first stage is responsible for installing the application's Python dependencies:

```dockerfile
FROM python:3.11-alpine AS build
```

A Python virtual environment is created and the dependencies from `requirements.txt` are installed.

The second stage starts from a clean Python image and copies the required environment and application files into it.

The basic process is:

```text
Build Stage
     |
     | Install dependencies
     v
Production Stage
     |
     | Copy application + environment
     v
Final Docker Image
```

This introduced me to multi-stage Docker builds and the idea of separating the build process from the final runtime environment.

---

## 📁 Project Structure

```text
docker-learning/
│
├── app.py
│
├── templates/
│   └── index.html
│
├── nginx.conf
│
├── Dockerfile
│
├── docker-compose.yml
│
├── requirements.txt
│
├── .dockerignore
│
├── .gitignore
│
└── README.md
```

### `app.py`

Contains the Flask application, routes and Redis connection.

### `templates/index.html`

Contains the portfolio interface and displays the visitor count using a Flask/Jinja template variable.

### `nginx.conf`

Contains the Nginx reverse proxy configuration.

### `Dockerfile`

Defines how the Flask Docker image is built.

### `docker-compose.yml`

Defines the Flask, Redis and Nginx services and their configuration.

### `requirements.txt`

Contains the Python dependencies.

### `.dockerignore`

Prevents unnecessary files such as `.venv`, `.git` and Python cache files from being included in the Docker build context.

### `.gitignore`

Prevents local development files and environment files from being committed to Git.

---

## 🖥️ The Website

I kept the frontend deliberately simple.

The purpose of this project wasn't to build a complicated frontend application. I wanted the website to provide a clean interface while the infrastructure behind it demonstrated the DevOps concepts.

The page contains:

### Introduction

A short introduction explaining that I'm building practical skills towards a Junior DevOps role.

### GitHub Button

A button linking directly to my GitHub profile.

### Technology Cards

The website explains the role of:

* Docker
* Redis
* Nginx

### Skills Section

The current technologies I'm working with include:

* Docker
* Docker Compose
* Linux
* Flask
* Redis
* Nginx
* Git
* CI/CD

### Architecture Section

The website also shows the basic application architecture:

```text
Browser
   ↓
Nginx
   ↓
Flask
   ↓
Redis
   ↓
Docker Volume
```

### Visitor Counter

The visitor counter is powered by Redis, so the number displayed on the website comes from the backend rather than being a static value in the HTML.

---

## ▶️ Running the Project Locally

### 1. Clone the repository

```bash
git clone https://github.com/AbdirahimGit/docker-learning.git
```

### 2. Enter the project

```bash
cd docker-learning
```

### 3. Build and start the application

```bash
docker compose up --build
```

### 4. Open the application

Go to:

```text
http://localhost:5002
```

---

## 🧪 Useful Docker Commands

### Start the application

```bash
docker compose up
```

### Build the Docker image

```bash
docker compose build
```

### Rebuild without using the build cache

```bash
docker compose build --no-cache
```

### Build and start everything

```bash
docker compose up --build
```

### Run in the background

```bash
docker compose up -d
```

### Stop the containers

```bash
docker compose down
```

### Check running services

```bash
docker compose ps
```

### View logs

```bash
docker compose logs
```

### View Flask logs

```bash
docker compose logs web
```

### View Redis logs

```bash
docker compose logs redis
```

### View Nginx logs

```bash
docker compose logs nginx
```

---

## 🧠 What I Learned

This project started as a simple Flask and Redis container challenge, but it gave me practical experience with several DevOps concepts.

### 1. Containerisation

I learned how to package a Python application into a Docker image along with its dependencies.

This means the application doesn't rely on the Python environment installed directly on my laptop.

### 2. Multi-container applications

I learned how to separate different responsibilities into different containers.

Instead of putting everything into one container, I have:

```text
Nginx
Flask
Redis
```

Each service has its own responsibility.

### 3. Docker networking

I learned how containers communicate through a Docker network and how Docker Compose provides service discovery.

For example:

```text
Flask → redis:6379
```

rather than:

```text
Flask → localhost:6379
```

### 4. Reverse proxies

Using Nginx helped me understand how a reverse proxy sits between the client and the application.

```text
Client
  ↓
Nginx
  ↓
Flask
```

### 5. Persistent storage

Using a Docker volume with Redis helped me understand why important application data shouldn't depend on the lifetime of a container.

### 6. Environment variables

The Redis connection details are configured through environment variables:

```text
REDIS_HOST
REDIS_PORT
```

This means the application configuration isn't hard-coded and can be changed depending on the environment.

### 7. Health checks

I learned how an application can expose a health endpoint that checks whether its dependencies are working.

In this case:

```text
Flask → Redis → Connected
```

### 8. Docker troubleshooting

I also had to troubleshoot issues while building the project.

Some of the problems I encountered included:

* Python packages not being recognised by VS Code
* Docker using an older image
* Docker build caching
* Docker Compose not finding a service to build
* Understanding container networking
* Understanding the difference between `localhost` and Docker service names
* Managing Git branches that had diverged from the remote repository

Working through these problems was useful because it forced me to understand what Docker and Git were actually doing instead of just following commands.

---

## 🔧 Challenges I Encountered

One of the most useful parts of this project was that it didn't work perfectly on the first attempt.

For example, I initially ran into a Docker Compose issue where:

```text
no configuration file provided
```

was returned because I was running the command from the wrong directory.

I also encountered:

```text
No services to build
```

which helped me understand the difference between specifying an `image` and specifying a `build` configuration in Docker Compose.

Another issue was Docker continuing to use an older application image. This introduced me to Docker's build cache and the use of:

```bash
docker compose build --no-cache
```

These small problems ended up being useful learning experiences.

---

## 📚 Skills Demonstrated

Through this project I've gained practical experience with:

* Docker
* Docker Compose
* Dockerfiles
* Multi-stage Docker builds
* Docker networking
* Docker volumes
* Python
* Flask
* Redis
* Nginx
* Reverse proxies
* Environment variables
* Health checks
* Linux
* Git
* GitHub
* Container troubleshooting
* Application debugging

I'm still developing these skills, but this project gave me a practical way to put several of them together in one application.

---

## 🔮 What I Would Add Next

There are a few things I'd like to build on top of this project.

### CI/CD

Create a GitHub Actions pipeline that automatically:

1. Runs tests
2. Builds the Docker image
3. Checks that the application is working
4. Pushes the image to a container registry

### Container Registry

Push the Docker image to GitHub Container Registry and learn how container images are stored and versioned.

### Cloud Deployment

Deploy the application to a Linux cloud server and make it accessible over the internet.

### HTTPS

Configure HTTPS with Nginx and learn more about certificates and secure traffic.

### Monitoring

Add application and container monitoring so I can see application health, logs and resource usage.

### Automated Testing

Add tests for the Flask routes and Redis functionality.

---

## 🎯 Why I Built This

The main goal wasn't to create a complicated application.

I wanted to understand what actually happens behind a web application when it is containerised.

Some of the questions I wanted this project to help me answer were:

* How do multiple containers communicate?
* How does Docker networking work?
* Why would I use Nginx in front of Flask?
* Where should application data be stored?
* What happens when a container is removed?
* How does Flask communicate with Redis?
* How do I rebuild an application after changing the code?
* How can I troubleshoot containers when something doesn't work?
* How could I eventually automate testing and deployment?

Building the project gave me a practical environment to explore those questions.

---

## 👨‍💻 Author

**Abdirahim**

Junior DevOps / Cloud Engineering learner

GitHub: [github.com/AbdirahimGit](https://github.com/AbdirahimGit)

---

## 📌 Project Status

This is an ongoing learning project.

The current version focuses on:

**Docker + Docker Compose + Flask + Redis + Nginx + Persistent Storage**

Future improvements will focus on:

**CI/CD + Testing + Container Registry + Cloud Deployment + Monitoring**
