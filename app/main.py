from fastapi import FastAPI


app = FastAPI(
    title="OPS Microservice",
    description="A lightweight service for monitoring and managing processing tasks.",
    version="1.0.0",
)


@app.get("/")
def read_root():
    return {
        "service": "OPS Microservice",
        "status": "online",
        "version": "1.0.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/status")
def service_status():
    return {
        "service": "OPS Microservice",
        "status": "operational",
        "environment": "local",
    }