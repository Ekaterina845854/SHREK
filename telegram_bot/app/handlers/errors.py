from aiogram import Router
from aiogram.types import ErrorEvent

router = Router()

@router.errors()
async def handle_errors(event: ErrorEvent):
    print(f"[ERROR] {event.exception}")
