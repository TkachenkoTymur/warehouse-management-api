from pydantic import BaseModel, field_validator
from pydantic import ValidationInfo
from datetime import date

class CreateUserModel(BaseModel):
    firstName: str
    lastName: str
    birthday: date

    @field_validator("firstName", "lastName")
    @classmethod
    def name_must_be_nonempty_and_letters(cls, v: str, info: ValidationInfo):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty")

        if not v.isalpha():
            raise ValueError(f"{info.field_name} must contain only letters")

        return v