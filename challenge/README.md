# CoderCo Containers Challenge

## Flask + Redis + Nginx

This was a CoderCo challenge where I built a small multi-container application using **Flask, Redis and Docker**.

The main goal was to get comfortable with running different parts of an application in separate containers and getting them to communicate with each other.

I also added **Nginx** as a reverse proxy to get some extra hands-on experience with how traffic can be routed to an application.

---

## What I Built

The application is a simple Flask app with two routes:

* `/` - shows a welcome message
* `/count` - keeps track of how many times the page has been visited

Redis is used to store the visit count.

The basic flow looks like this:

```text
Browser
   |
   v
 Nginx
   |
   v
 Flask
   |
   v
 Redis
```

So when I visit `/count`, the request goes through Nginx to Flask. Flask then talks to Redis, gets the current count, increments it, and returns the new count.

---

## Technologies Used

* **Python / Flask** - web application
* **Redis** - stores the visit count
* **Nginx** - reverse proxy
* **Docker** - runs each service in a container
* **Docker Compose** - manages the containers
* **Git / GitHub** - version control

---

## How the Visit Counter Works

The `/count` route uses Redis to keep track of the number of visits.

For example, the first time I visit:

```text
/count
```

Redis might contain:

```text
visits = 1
```

Refreshing the page causes Flask to ask Redis for the current value and increment it:

```text
visits = 2
```

Refresh again:

```text
visits = 3
```

And so on.

The important part here is that **Flask isn't keeping the count itself**. Redis is responsible for storing it.

This means that each time Flask receives a request, it can get the current value from Redis, update it, and return the new value.

---

## Redis Volume

One thing I learned from this challenge was the difference between **data inside a container** and **persistent data**.

Redis normally stores its data in memory. That means the counter can be updated very quickly, which is one of the reasons Redis is useful.

However, containers are designed to be replaceable.

If I remove the Redis container, the data inside that container can disappear.

That's where a **Docker volume** comes in.

The volume gives Redis a place outside the container's temporary filesystem where its persisted data can be stored.

The setup is roughly:

```text
Redis Container
      |
      v
Docker Volume
      |
      v
Persistent Redis Data
```

So if Redis is restarted or the container is recreated, the volume can allow Redis to recover its persisted data.

### Why do I need it?

For the counter itself, the volume is **not what makes the number increase when I refresh the page**.

The increment happens because:

```text
Browser
   ↓
Flask
   ↓
Redis
   ↓
GET current count
   ↓
INCREMENT count
   ↓
Store updated count
   ↓
Return response
```

Redis keeps the current value while it is running.

The volume becomes important when I want that data to **survive beyond the lifetime of the Redis container**.

For example:

```text
Without volume:

Redis container
    ↓
Container deleted
    ↓
Stored data can be lost
    ↓
Counter starts again
```

With a volume:

```text
Redis container
    ↓
Docker volume
    ↓
Container deleted/recreated
    ↓
Volume still exists
    ↓
Redis can load its persisted data
```

This was a useful lesson for me because I initially thought of the volume as being responsible for updating the counter. It isn't. **Redis handles the counter; the volume is there for persistence.**

---

## Docker Compose

I used Docker Compose to run the different services together.

Instead of having to manually start each container, I can bring the application up with:

```bash
docker compose up
```

And stop the services with:

```bash
docker compose down
```

This also made it easier to define things like:

* Which containers are part of the application
* Which ports are exposed
* How the containers communicate
* Environment variables
* Redis volumes
* Service dependencies

---

## Nginx

I added Nginx to the project to understand how a reverse proxy works.

Without Nginx, the request would look something like:

```text
Browser → Flask
```

With Nginx:

```text
Browser → Nginx → Flask
```

Nginx receives the request and forwards it to the Flask application.

This was useful because it gave me some exposure to a setup that is closer to how web applications are commonly structured in production.

---

## Docker Networking

Another thing I learned was how containers communicate with each other.

At first, it's easy to think that Flask should connect to:

```text
localhost
```

when trying to reach Redis.

But inside Docker, `localhost` refers to the **Flask container itself**, not the Redis container.

Instead, Docker Compose creates a network where services can communicate using their service names.

So Flask can connect to Redis using something like:

```text
redis:6379
```

rather than trying to connect to localhost.

That was one of the more useful concepts I took away from this challenge.

---

## What I Learned

This challenge helped me understand Docker beyond just running a single container.

Some of the main things I learned were:

### Docker

How to build and run containers and package an application with its dependencies.

### Docker Compose

How multiple containers can be managed as one application.

### Flask

How a simple Python web application handles requests and communicates with another service.

### Redis

How Redis can be used as a fast key-value store and how an application can read and update values stored in it.

### Volumes

How Docker volumes can be used when data needs to survive beyond the lifecycle of a container.

### Networking

How containers communicate with each other over a Docker network and why `localhost` doesn't mean the same thing across containers.

### Nginx

How a reverse proxy sits in front of an application and forwards requests to the appropriate service.

### Debugging

I also got more comfortable using Docker commands to investigate what was happening inside the application:

```bash
docker ps
docker logs <container>
docker compose logs
docker exec -it <container> sh
```

---

## Testing the Application

The application can be accessed locally through the configured port.

### Welcome page

```text
http://localhost:5002
```

### Visit counter

```text
http://localhost:5002/count
```

Refreshing `/count` should increase the visit count.

---

## Takeaway

The biggest thing I took from this challenge was understanding how the different pieces fit together.

Instead of thinking of the application as just a Flask program, I started thinking about it as several services working together:

```text
             Nginx
               |
               v
             Flask
               |
               v
             Redis
               |
               v
             Volume
```

Each part has its own job, and Docker provides the environment for them to run and communicate with each other.

This gave me a much better understanding of **containers, networking, persistence, reverse proxies, and multi-container application architecture**.
