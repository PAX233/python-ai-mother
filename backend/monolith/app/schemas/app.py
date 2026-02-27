from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.user import UserVO


class AppAddRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    init_prompt: str | None = Field(default=None, alias="initPrompt")


class AppVO(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: int
    app_name: str = Field(alias="appName")
    cover: str | None = None
    init_prompt: str | None = Field(default=None, alias="initPrompt")
    code_gen_type: str = Field(alias="codeGenType")
    deploy_key: str | None = Field(default=None, alias="deployKey")
    deployed_time: datetime | None = Field(default=None, alias="deployedTime")
    priority: int = 0
    user_id: int = Field(alias="userId")
    create_time: datetime | None = Field(default=None, alias="createTime")
    update_time: datetime | None = Field(default=None, alias="updateTime")
    user: UserVO | None = None


class ChatToGenCodeParams(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    app_id: int = Field(alias="appId")
    message: str
