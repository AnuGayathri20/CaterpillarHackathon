import firebase_admin
from firebase_admin import credentials, auth
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.security import OAuth2PasswordBearer

oauthContext=OAuth2PasswordBearer(tokenUrl="token")

cred = credentials.Certificate("caterpillar-65dcc-firebase-adminsdk-q4ge4-cf012c8de5.json")
firebase_admin.initialize_app(cred)

class FirebaseAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in {"/docs", "/openapi.json"}:
            response = await call_next(request)
            return response

        try:
            token = await oauthContext(request)
        except Exception:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})

        if token:
            try:
                decoded_token = auth.verify_id_token(token)
                request.state.user = decoded_token['user_id']
            except Exception as e:
                return JSONResponse(status_code=401, content={"detail": "Invalid token"})
        else:
            return JSONResponse(status_code=401, content={"detail": "Authorization header missing or invalid"})

        response = await call_next(request)
        return response