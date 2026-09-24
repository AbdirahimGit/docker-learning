import os
from flask import Flask
import redis

app = Flask(__name__)

redis_host = os.getenv ('REDIS _HOST', 'redis')
redis_port = int(os.getenv('REDIS_PORT', 6379))
redis_count=redis.Redis (host=redis_host, port=redis_port)
    

@app.route('/')
def hello_world():
    return 'CoderCo Containers Session!'

@app.route('/count')
def count():
    visits = redis_count.incr("visit_count")

    return f"Hello! This page has been visited {visits} times."

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
