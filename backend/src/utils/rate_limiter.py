import time
from collections import defaultdict, deque
from typing import Dict, Deque
from fastapi import HTTPException, status
import threading


class RateLimiter:
    def __init__(self):
        self.requests: Dict[str, Deque[float]] = defaultdict(deque)
        self.lock = threading.Lock()

    def is_allowed(self, identifier: str, max_requests: int, window_size: int) -> bool:
        """
        Check if a request from the given identifier is allowed based on rate limits.

        Args:
            identifier: Unique identifier for the requester (e.g., IP address, user ID)
            max_requests: Maximum number of requests allowed
            window_size: Time window in seconds

        Returns:
            True if request is allowed, False otherwise
        """
        with self.lock:
            now = time.time()
            window_start = now - window_size

            # Remove old requests outside the window
            while self.requests[identifier] and self.requests[identifier][0] < window_start:
                self.requests[identifier].popleft()

            # Check if we've exceeded the limit
            if len(self.requests[identifier]) >= max_requests:
                return False

            # Add the current request
            self.requests[identifier].append(now)
            return True


# Global rate limiter instance
rate_limiter = RateLimiter()


def check_rate_limit(identifier: str, max_requests: int = 100, window_size: int = 60):
    """
    Check rate limit for a given identifier.

    Args:
        identifier: Unique identifier for the requester
        max_requests: Maximum number of requests allowed (default: 100)
        window_size: Time window in seconds (default: 60)

    Raises:
        HTTPException: If rate limit is exceeded
    """
    if not rate_limiter.is_allowed(identifier, max_requests, window_size):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later."
        )