from fastapi.security import OAuth2PasswordBearer

# OAuth2PasswordBearer is a security flow. It defines where the token is retrieved.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/auth/login"
)
