from textwrap import dedent
from typing import List, Dict

from google import genai
from google.genai import types

from app.config.settings import GEMINI_API_KEY, GEMINI_MODEL
from app.exceptions.custom_exception import CustomException
from app.exceptions.error_code import ErrorCode
from app.exceptions.status_code import StatusCode

class NewsSummarizer:
    """
    기업 뉴스 요약기
    """

    def summarize(self, articles: List[Dict]) -> str:
        """
        articles:
        [
          {
            "title": str,
            "content": str,
            ...
          }
        ]
        """

        if not articles:
            return "수집된 기사가 없습니다."

        merged_text = self._merge_articles(articles)
        prompt = self._build_prompt(merged_text)

        return self._generate_summary(prompt)

    def _generate_summary(self, prompt: str) -> str:
        """
        LLM 생성
        """
        client = genai.Client(api_key=GEMINI_API_KEY)

        try:
            response = client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    top_p=0.9,
                    max_output_tokens=1024,
                    response_mime_type="text/plain",
                )
            )
        except Exception as e:
            raise CustomException(
                StatusCode.INTERNAL_SERVER_ERROR,
                ErrorCode.GEMINI_API_ERROR,
                detail=str(e)
            ) from e

        return response.text

    def _merge_articles(self, articles: List[Dict]) -> str:
        """
        기사들을 하나의 텍스트로 병합
        """
        texts = []

        for idx, article in enumerate(articles, start=1):
            title = article.get("title", "")
            content = article.get("content", "")
            texts.append(f"[기사 {idx}]\n제목: {title}\n내용: {content}")

        return "\n\n".join(texts)

    def _build_prompt(self, merged_text: str) -> str:
        """
        LLM에 전달할 메시지 생성
        """
        return dedent(f"""
다음은 특정 기업과 관련된 뉴스 기사 모음이다.

역할:
당신은 금융 및 경제 뉴스를 요약하는 전문가이다.

지시사항:
- 여러 기사에서 중복되는 내용은 제거한다.
- 핵심 이슈 중심으로 요약한다.
- 중요한 사건은 시간 순서를 고려하여 정리한다.
- 불필요한 수식어나 반복 표현은 제거한다.
- 5~10줄 정도로 작성하되, 필요한 경우 최대 20줄까지 작성한다.
- 한국어로 작성한다.

기사:
{merged_text}
""")