import fastapi

api = fastapi.FastAPI()


@api.get("/")
def read_root():
    return {"Hello": "World"}

# ses = boto3.resource("sesv2")


# class User(model.HashModel):
#     username: StrictStr = model.Field(index=True, regex=r"[\w\-\.]+")
#     recovery_email: EmailStr

# def add_new_user(username: str, recovery_email: str) -> None:
#     if User.find(User.username == username).all():
#         raise ValueError("Username already exists")
#     else:
#         User(username=username, recovery_email=recovery_email).save()


# def request_new_email(username: str) -> str:
#     # https://boto3.amazonaws.com/v1/documentation/api/latest/reference
#     # /services/sesv2.html#SESV2.Client.create_email_identity
#     try:
#         address = f"{username}@{settings.config.domain}"
#         response = ses.create_email_identity(address)
#     except exceptions.ClientError:
#         pass
