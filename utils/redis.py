import redis as redis_py

# Redis config
redis = redis_py.Redis(
    host="127.0.0.1", port=6379, db=0
)
