from fastapi import FastAPI, HTTPException
import redis
import uuid
import os

app = FastAPI()

# Bug Fix: Use environment variables for Redis connection
REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
QUEUE_NAME = os.getenv("QUEUE_NAME", "job_queue")

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

@app.get("/health")
def health_check():
    try:
        r.ping()
        return {"status": "healthy"}
    except:
        raise HTTPException(status_code=500, detail="Redis unreachable")

@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    # Bug Fix: Set status in Hash FIRST, then push to queue to avoid race conditions
    r.hset(f"job:{job_id}", mapping={"status": "queued", "id": job_id})
    r.lpush(QUEUE_NAME, job_id)
    return {"job_id": job_id}

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    # Bug Fix: Handle cases where job_id doesn't exist gracefully
    if status is None:
        return {"error": "Job not found"}, 404
    return {"job_id": job_id, "status": status.decode()}
