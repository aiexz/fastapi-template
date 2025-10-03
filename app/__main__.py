import contextlib
import os

import fastapi
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.semconv.attributes.service_attributes import SERVICE_NAME
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.system_metrics import SystemMetricsInstrumentor
from prometheus_client import start_http_server

from app.database.methods import Database


def setup_telemetry():
    # Set up tracing
    trace.set_tracer_provider(TracerProvider(
    resource=Resource.create({SERVICE_NAME: os.getenv('SERVICE_NAME', 'fastapi-app')})
))
    
    # Configure OTLP exporters
    otlp_metrics_endpoint = os.getenv("OTPL_METRICS_ENDPOINT", "http://localhost:8428/opentelemetry/v1/metrics") # VictoriaMetrics

    otlp_trace_endpoint = os.getenv("OTPL_TRACE_ENDPOINT", "http://localhost:4317/v1/traces") # Grafana Tempo

    
    # Trace exporter
    otlp_trace_exporter = OTLPSpanExporter(endpoint=otlp_trace_endpoint, insecure=True)
    trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_trace_exporter))
    
    # Metrics exporter
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=otlp_metrics_endpoint)
    )
    metrics.set_meter_provider(MeterProvider(metric_readers=[metric_reader]))



def setup_routes(fastaApiApp: fastapi.FastAPI):
    import app.routes.health
    import app.routes.index

    fastaApiApp.include_router(app.routes.health.router)
    fastaApiApp.include_router(app.routes.index.router)


def setup_dependencies(fastaApiApp: fastapi.FastAPI):
    import app.dependancies

    database = Database(
            os.getenv(
                    "DATABASE_URL",
                    "postgresql+psycopg://postgres:postgres@localhost:5432/postgres",
            ))
    fastaApiApp.dependency_overrides[app.dependancies.DatabaseDependency] = lambda: database()
    # Instrument SQLAlchemy
    SQLAlchemyInstrumentor().instrument(engine=database.engine.sync_engine)

@contextlib.asynccontextmanager
async def lifespan_wrapper(fastapi_app: fastapi.FastAPI):
    import app.dependancies
    # do stuff here
    yield
    # do stuff here
    # e.g. close database connections, clean up resources, etc.
    await fastapi_app.dependency_overrides[app.dependancies.DatabaseDependency]().engine.dispose()

app = fastapi.FastAPI(lifespan=lifespan_wrapper)

# Set up OpenTelemetry
setup_telemetry()

setup_dependencies(app)
setup_routes(app)

# Instrument FastAPI with both traces and metrics
FastAPIInstrumentor.instrument_app(app, meter_provider=metrics.get_meter_provider())
