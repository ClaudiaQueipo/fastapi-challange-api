import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class ResponseTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        seconds = process_time
        if seconds >= 3600:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            secs = seconds % 60
            time_str = f"{hours} h {minutes} min {secs:.4f} sec"
        elif seconds >= 60:
            minutes = int(seconds // 60)
            secs = seconds % 60
            time_str = f"{minutes} min {secs:.4f} sec"
        else:
            time_str = f"{seconds:.4f} seconds"
        logger.info(f"Request to {request.url} took {time_str}")
        return response
