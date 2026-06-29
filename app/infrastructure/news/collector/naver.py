import requests
import time
import html
from datetime import datetime
from email.utils import parsedate_to_datetime
from typing import Dict, List, Optional

from bs4 import BeautifulSoup

from app.config.settings import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET
from app.infrastructure.news.collector.base import NewsCollector
from app.infrastructure.news.rate_limiter import RateLimiter

class NaverNewsCollector(NewsCollector):
    BASE_URL = "https://openapi.naver.com/v1/search/news.json"

    def __init__(self, rate_limiter: RateLimiter):
        super().__init__()
        self.rate_limiter = rate_limiter

    def collect(
            self,
            keyword: str,
            start_time: datetime,
            end_time: datetime,
            max_articles: int = 50
    ) -> List[Dict]:

        articles = []
        start = 1

        while len(articles) < max_articles:
            if start > 1000:  # Naver API 제한
                break

            params = {
                "query": keyword,
                "display": min(10, max_articles - len(articles)),
                "start": start,
                "sort": "date"
            }

            headers = {
                "X-Naver-Client-Id": NAVER_CLIENT_ID,
                "X-Naver-Client-Secret": NAVER_CLIENT_SECRET,
            }

            resp = self._safe_get(self.BASE_URL, params=params, headers=headers)

            if not resp:
                break

            data = resp.json()
            items = data.get("items", [])

            if not items:
                break

            for item in items:

                try:
                    published_at = parsedate_to_datetime(
                        item["pubDate"]
                    ).replace(tzinfo=None)
                except Exception:
                    continue

                if published_at < start_time:
                    return articles

                if published_at > end_time:
                    continue

                url = item.get("originallink") or item.get("link")

                article = self._fetch_article(url, published_at)

                if article:
                    articles.append(article)

                if len(articles) >= max_articles:
                    break

            start += 10

        return articles

    def _fetch_article(self, url: str, published_at: datetime) -> Optional[Dict]:
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
        except requests.RequestException:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # fallback 구조
        title_tag = (
            soup.select_one("h1")
            or soup.select_one("title")
        )

        content_tag = (
            soup.select_one("article")
            or soup.select_one("#content")
            or soup.select_one(".content")
        )

        if not title_tag or not content_tag:
            return None

        return {
            "title": html.unescape(title_tag.get_text(strip=True)),
            "content": content_tag.get_text(" ", strip=True),
            "published_at": published_at,
            "url": url,
            "source": "naver",
        }

    def _safe_get(self, url, params=None, headers=None, max_retry=3):
        for i in range(max_retry):
            self.rate_limiter.wait()

            try:
                resp = self.session.get(
                    url,
                    params=params,
                    headers=headers,
                    timeout=10
                )

                if resp.status_code == 429:
                    time.sleep(2 ** i)
                    continue

                resp.raise_for_status()
                return resp

            except requests.RequestException:
                time.sleep(2 ** i)

        return None
