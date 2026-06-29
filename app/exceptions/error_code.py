from enum import Enum

class ErrorCode(Enum):
    UNKNOWN_ERROR = ("UNKNOWN_ERROR", "Unknown error.")

    # User
    INVALID_USER = ("INVALID_USER", "Invalid user.")
    SESSION_EXPIRED = ("SESSION_EXPIRED", "Session expired.")

    # Company
    COMPANY_NOT_FOUND = ("COMPANY_NOT_FOUND", "Company not found.")
    COMPANY_NAME_NOT_FOUND = ("COMPANY_NAME_NOT_FOUND", "Company name not found.")

    # Daily Sentiment
    DAILY_SENTIMENT_NOT_FOUND = ("DAILY_SENTIMENT_NOT_FOUND", "Daily sentiment not found.")

    # News
    NEWS_NOT_FOUND = ("NEWS_NOT_FOUND", "News not found.")
    UNSUPPORTED_NEWS_SOURCE = ("UNSUPPORTED_NEWS_SOURCE", "Unsupported news source.")

    # Request
    INVALID_PARAMETER = ("INVALID_PARAMETER", "Invalid parameter.")

    # Server
    INTERNAL_SERVER_ERROR = ("INTERNAL_SERVER_ERROR", "Internal server error.")

    # External API
    GEMINI_API_ERROR = ("GEMINI_API_ERROR", "Failed to generate content from Gemini.")

    CRAWLING_ERROR = ("CRAWLING_ERROR", "Failed to crawl news.")
    DATABASE_ERROR = ("DATABASE_ERROR", "Database operation failed.")
    MODEL_INFERENCE_ERROR = ("MODEL_INFERENCE_ERROR", "Model inference failed.")

    def __init__(self, code: str, message: str):
        self.code = code
        self.message = message