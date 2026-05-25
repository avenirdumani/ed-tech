from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.core.exceptions import ConflictError, NotFoundError, CredentialError
from src.app.routes import applications, profiles, programs, users
from src.helpers import create_all_models


@asynccontextmanager
async def lifespan(app: FastAPI):

    create_all_models()
    yield


app = FastAPI(title="Admissions Readiness API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(CredentialError)
async def credential_handler(request: Request, exc: CredentialError):
    return JSONResponse(
        status_code=401, content={"detail": "Could not validate credentials"}
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})


app.include_router(programs.router)
app.include_router(profiles.router)
app.include_router(applications.router)
app.include_router(users.router)
