import os
from traceloop.sdk import Traceloop


def init_observability():
    Traceloop.init(disable_batch=True,
                   api_key=os.getenv("TRACER_API_KEY"),
                   )
