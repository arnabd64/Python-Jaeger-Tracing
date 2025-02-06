from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

# Setup Telemetry
attributes = {
    ResourceAttributes.SERVICE_NAME: "fibonacci-generator",
    ResourceAttributes.SERVICE_VERSION: "0.1",
    ResourceAttributes.DEVICE_ID: "39053IBF37",
    "Author": "aranbd64"
}
provider = TracerProvider(resource=Resource(attributes=attributes))
trace.set_tracer_provider(provider)
exporter = OTLPSpanExporter("localhost:4317", insecure=True)
span_processor = BatchSpanProcessor(exporter)
provider.add_span_processor(span_processor)

tracer = trace.get_tracer(__name__)


def fibonacci(n: int) -> list[int]:
    with tracer.start_as_current_span("fibonacci") as span:
        span.set_attribute("input.n", n)
        if not isinstance(n, int):
            raise TypeError("n must be an integer")
        if n < 0:
            raise ValueError("n must be non-negative")
        if n == 0:
            result = []
        elif n == 1:
            result = [0]
        else:
            result = fibonacci(n - 1)
            result.append(result[-1] + result[-2] if len(result) > 1 else 1)
        span.set_attribute("result", str(result))
        return result
    
if __name__ == "__main__":
    N = 15
    print(fibonacci(N))