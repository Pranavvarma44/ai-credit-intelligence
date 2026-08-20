from pydantic import BaseModel, EmailStr, Field


# --------------------------------------------------
# REGISTER REQUEST
# --------------------------------------------------

class UserCreate(BaseModel):

    name: str

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=72
    )


# --------------------------------------------------
# LOGIN REQUEST
# --------------------------------------------------

class UserLogin(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=1,
        max_length=72
    )


# --------------------------------------------------
# USER RESPONSE
# --------------------------------------------------

class UserResponse(BaseModel):

    id: int

    name: str

    email: EmailStr