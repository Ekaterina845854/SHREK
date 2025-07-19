from app.config import config
from app.src.api.archetypes.controller import app as archetypes_controller
from app.src.api.characters.controller import app as characters_controller
from app.src.api.styles.controller import app as styles_controller
from app.src.api.tasks.controller import app as tasks_controller
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    archetypes_controller, tags=["Archetypes"],
)
app.include_router(
    styles_controller, tags=["Styles"],
)
app.include_router(
    characters_controller, tags=["Characters"],
)
app.include_router(
    tasks_controller, tags=["Tasks"]
)