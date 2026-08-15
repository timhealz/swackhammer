"""Simple caching utilities for expensive API calls."""

from __future__ import annotations

from functools import wraps
from typing import Any, Callable, Dict, Hashable, Tuple

try:
    from diskcache import Cache
except Exception:  # pragma: no cover - diskcache should be installed
    Cache = None  # type: ignore[assignment]

_CACHE_PATH = ".cache"

if Cache is not None:
    _CACHE = Cache(_CACHE_PATH)
else:  # pragma: no cover - fallback used if diskcache missing
    _CACHE = {}  # type: ignore[var-annotated]


def _make_key(name: str, args: Tuple[Any, ...], kwargs: Dict[str, Any]) -> Hashable:
    return (name, args, frozenset(sorted(kwargs.items())))


def cached(ttl: int = 3600) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Cache the return value of the wrapped function for ``ttl`` seconds."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        cache_backend = _CACHE

        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            key = _make_key(func.__name__, args, kwargs)
            if isinstance(cache_backend, dict):
                if key in cache_backend:
                    return cache_backend[key]
                result = func(*args, **kwargs)
                cache_backend[key] = result
                return result

            cached_result = cache_backend.get(key)
            if cached_result is not None:
                return cached_result

            result = func(*args, **kwargs)
            cache_backend.set(key, result, expire=ttl)
            return result

        return wrapper

    return decorator


__all__ = ["cached"]
