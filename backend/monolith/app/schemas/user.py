from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_account: str | None = Field(default=None, alias="userAccount")
    user_password: str | None = Field(default=None, alias="userPassword")
    check_password: str | None = Field(default=None, alias="checkPassword")


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    user_account: str | None = Field(default=None, alias="userAccount")
    user_password: str | None = Field(default=None, alias="userPassword")


class LoginUserVO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    user_account: str = Field(alias="userAccount")
    user_name: str | None = Field(default=None, alias="userName")
    user_avatar: str | None = Field(default=None, alias="userAvatar")
    user_profile: str | None = Field(default=None, alias="userProfile")
    user_role: str = Field(alias="userRole")
    create_time: datetime | None = Field(default=None, alias="createTime")
    update_time: datetime | None = Field(default=None, alias="updateTime")
