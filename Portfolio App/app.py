import os
from flask import Flask, render_template
import redis

app = Flask(__name__)

# Redis configuration
redis_host = os.getenv("REDIS_HOST", "redis")
redis_port = int(os.getenv("REDIS_PORT", 6379))

redis_count = redis.Redis(
    host=redis_host,
    port=redis_port,
    decode_responses=True
)


@app.route("/")
def home():
    visits = redis_count.incr("portfolio_visits")

    return render_template(
        "index.html",
        visits=visits
    )


@app.route("/count")
def count():
    visits = redis_count.incr("visit_count")

    return f"This page has been visited {visits} times."


@app.route("/health")
def health():
    try:
        redis_count.ping()

        return {
            "status": "healthy",
            "redis": "connected"
        }, 200

    except redis.RedisError:

        return {
            "status": "unhealthy",
            "redis": "disconnected"
        }, 503


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5002
    )

