import redis
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(name="DNS Server")
redis_instance = redis.Redis(host='localhost', port=6379, decode_responses=True)

class DomainData(BaseModel):
    domain: str
    ip: str

@app.post("/dns")
async def add_domain(domain_data: DomainData):
    domain = domain_data.domain
    ip = domain_data.ip

    if redis_instance.get(domain):
        raise HTTPException(status_code=400, detail="Domain already exists")

    redis_instance.set(domain, ip)

    return {"message": f"Domain '{domain}' with IP '{ip}' has been added."}


@app.delete("/dns")
async def delete_domain(domain_data: DomainData):
    domain = domain_data.domain

    if not redis_instance.get(domain):
        raise HTTPException(status_code=400, detail="Domain not found")

    redis_instance.delete(domain)

    return {"message": f"Domain '{domain}' has been deleted."}
