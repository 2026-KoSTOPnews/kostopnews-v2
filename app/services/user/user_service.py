from datetime import datetime

from sqlalchemy.orm import Session

from app.exceptions.custom_exception import CustomException
from app.exceptions.error_code import ErrorCode
from app.exceptions.status_code import StatusCode
from app.infrastructure.db.repositories.user_repository_impl import SqlAlchemyUserSentimentRepository as UserSentimentRepository
from app.infrastructure.db.repositories.company_repository_impl import SqlAlchemyCompanyRepository as CompanyRepository
from app.services.user.user_pipeline import UserSentimentPipeline

class UserSentimentService:
    def __init__(self, db: Session, pipeline:UserSentimentPipeline = None):
        self.db = db
        self.repository = UserSentimentRepository(db)
        self.company_repository = CompanyRepository(db)
        self.pipeline = pipeline

    def get_user_sentiments_by_user_id(self, user_id: str):
        sentiments = self.repository.find_all_by_user_id(user_id)
        return sentiments

    def get_user_sentiments_by_keyword_and_user_id(self, keyword: str, user_id: str):
        sentiments = self.repository.find_all_by_keyword_and_user_id(keyword, user_id)
        return sentiments

    def create_user_sentiment(self, result):
        sentiment = self.repository.save_user_sentiment(result)
        return sentiment

    def run_user(self, user_id: str, company_name: str, request_time: datetime | None = None):
        company = self.company_repository.find_by_name(company_name)

        if company is None:
            raise CustomException(
                StatusCode.NOT_FOUND,
                ErrorCode.COMPANY_NAME_NOT_FOUND,
                detail=f"Company Name: {company_name}",
            )

        try:
            result = self.pipeline.run_for_user(
                user_id=user_id,
                company_id=company.id,
                company_name=company_name,
                request_time=request_time
            )

            saved = self.create_user_sentiment(result)

            return saved

        except Exception as e:
            raise CustomException(
                StatusCode.INTERNAL_SERVER_ERROR,
                ErrorCode.UNKNOWN_ERROR,
                detail=str(e)
            )
