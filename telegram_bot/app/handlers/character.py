from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.forms import (CreateCharacterForm, MainForm, ManageCharactersForm,
                       SelectCharacterForm)
from app.keyboards import main_menu
from app.services import character
# from services.llm_api import ask_character
from app.utils.texts import texts

router = Router()

@router.message(Command("create_character"))
async def cmd_create_character(message: Message, state: FSMContext):
   await character.create_character_step_0(message, state)


@router.message(MainForm.manage_characters, F.text == "Создать нового персонажа")
async def create_character(message: Message, state: FSMContext):
    await character.create_character_step_0(message, state)

@router.message(CreateCharacterForm.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await character.create_character_step_1(message, state)


@router.callback_query(CreateCharacterForm.waiting_for_archetype, F.data.startswith("archetype:"))
async def process_archetype(callback: CallbackQuery, state: FSMContext):
    await character.create_character_step_2(callback, state)


@router.callback_query(CreateCharacterForm.waiting_for_style, F.data.startswith("style:"))
async def process_style(callback: CallbackQuery, state: FSMContext):
    await character.create_character_step_3(callback, state)


@router.message(F.text == "Управление персонажами")
async def manage_characters(message: Message, state: FSMContext):
    await character.manage_characters(message, state)
    

@router.message(MainForm.manage_characters, F.text == "Посмотреть всех персонажей")
async def show_all_characters(message: Message):
    await character.show_all_characters(message)
    

@router.callback_query(F.data.startswith("show_character:"))
async def show_character(callback: CallbackQuery):
    await character.show_character(callback)
    

@router.message(MainForm.manage_characters, F.text == "Удалить персонажа")
async def show_all_characters(message: Message, state: FSMContext):
    await character.show_all_removable_characters(message, state)
    
    
@router.callback_query(ManageCharactersForm.delete_characters, F.data.startswith("delete_character:"))
async def ask_deleting_character(callback: CallbackQuery, state: FSMContext):
    await character.ask_approve_deleting(callback, state)


@router.callback_query(ManageCharactersForm.approve_deleting, F.data == "delete_character:approve")
async def delete_character(callback: CallbackQuery, state: FSMContext):
    await character.delete_character(callback, state)
    

@router.callback_query(ManageCharactersForm.approve_deleting, F.data == "delete_character:cancel")
async def cancel_deleting_character(callback: CallbackQuery, state: FSMContext):
    await character.cancel_deleting_character(callback, state)
    

@router.message(F.text == "Выбрать персонажа")
async def start_select_character(message: Message, state: FSMContext):
    await character.start_select_character(message, state)
    

@router.callback_query(MainForm.select_character, F.data.startswith("select_character:"))
async def ask_selecting_character(callback: CallbackQuery, state: FSMContext):
    await character.ask_selecting_character(callback, state)
    
@router.callback_query(SelectCharacterForm.select_character_approve, F.data == ("select_character:approve"))
async def select_character(callback: CallbackQuery, state: FSMContext):
    await character.select_character(callback, state)
    

@router.callback_query(SelectCharacterForm.select_character_approve, F.data == ("select_character:cancel"))
async def cancel_select_character(callback: CallbackQuery, state: FSMContext):
    await character.cancel_select_character(callback, state)