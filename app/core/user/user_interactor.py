import uuid
from dataclasses import dataclass
from typing import Optional, Protocol

from app.core.entities import Response, UserInfo
from app.core.user.user_repository import IUserRepository


@dataclass
class RegisterUserRequest:
    email: str


@dataclass
class RegisterUserResponse(Response):
    api_key: Optional[str]


class IUserInteractor(Protocol):
    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        pass


class UserInteractor:
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository

    def register_user(self, request: RegisterUserRequest) -> RegisterUserResponse:
        if self.user_repository.get_user_by_email(request.email):
            return RegisterUserResponse(
                success=False,
                message="User with this email already exists",
                status_code=409,
                api_key=None,
            )

        api_key = str(uuid.uuid4().hex)
        user = UserInfo(email=request.email, api_key=api_key)
        self.user_repository.register_user(user)
        return RegisterUserResponse(
            api_key=api_key,
            success=True,
            status_code=201,
            message="Here is your api key, keep it safe!",
        )
