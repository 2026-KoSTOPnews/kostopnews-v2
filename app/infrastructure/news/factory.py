from typing import Dict, Type, List

from app.exceptions.custom_exception import CustomException
from app.exceptions.error_code import ErrorCode
from app.exceptions.status_code import StatusCode
from app.infrastructure.news.collector.base import NewsCollector
from app.infrastructure.news.collector.naver import NaverNewsCollector
from app.infrastructure.news.rate_limiter import RateLimiter

class NewsCollectorFactory:
    _collectors: Dict[str, Type[NewsCollector]] = {
        "naver": NaverNewsCollector(RateLimiter()),
    }

    @classmethod
    def create(cls, source: str) -> NewsCollector:
        source = source.lower()

        if source not in cls._collectors:
            raise CustomException(
                StatusCode.BAD_REQUEST,
                ErrorCode.UNSUPPORTED_NEWS_SOURCE,
                detail=f"Unsupported news source: {source}"
            )

        return cls._collectors[source]()

    @classmethod
    def create_all(cls) -> List[NewsCollector]:
        return list(cls._collectors.values())
        # return [collector() for collector in cls._collectors.values()]

    @classmethod
    def supported_sources(cls) -> List[str]:
        return list(cls._collectors.keys())
