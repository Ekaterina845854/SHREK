from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.forms import MainForm
from app.services.chat import create_task

router = Router()


@router.message(MainForm.chat_character)
async def handle_any_message(message: Message, state: FSMContext):
    await create_task(message, state)
