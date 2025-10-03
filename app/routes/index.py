from fastapi import APIRouter, Request
from opentelemetry import metrics

meter = metrics.get_meter(__name__)

total_requests = meter.create_counter(
    name="app_requests_total",
    description="Total number of requests",
    unit="1",
)

router = APIRouter()
@router.get("/")
async def root(request: Request):
    total_requests.add(1, {"endpoint": "/", "method": request.method})
    return {"message": "Hello World"}