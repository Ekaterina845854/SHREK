from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.forms import MainForm
from app.keyboards import main_menu
# from services.llm_api import ask_character
from app.utils.texts import texts

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts["start"], reply_markup=main_menu)


@router.message(Command("menu"))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts["menu"]["main"], reply_markup=main_menu)


@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts["help"])
    

@router.message(F.text == "Главное меню")
async def show_main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts["menu"]["main"], reply_markup=main_menu)
    

@router.message(MainForm.manage_characters, F.text == "Назад")
async def exit_manage_characters(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(texts["menu"]["main"], reply_markup=main_menu)
