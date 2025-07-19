from typing import Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from app import keyboards
from app.forms import (CreateCharacterForm, MainForm, ManageCharactersForm,
                       SelectCharacterForm)
from app.utils import structures
from app.utils.api import API
# from services.llm_api import ask_character
from app.utils.texts import texts


async def create_character_step_0(message: Message, state: FSMContext):
    await message.answer(texts["create_character"]["step_0"], reply_markup=ReplyKeyboardRemove())
    await state.set_state(CreateCharacterForm.waiting_for_name)
    

async def create_character_step_1(message: Message, state: FSMContext):
    await state.update_data(name=message.text)

    archetypes = await API.get_archetypes()
    keyboard = keyboards.archetypes_keyboard(archetypes)
    
    await message.answer(texts["create_character"]["step_1"], reply_markup=keyboard)
    
    await state.set_state(CreateCharacterForm.waiting_for_archetype)


async def create_character_step_2(callback: CallbackQuery, state: FSMContext):
    await state.update_data(archetype=int(callback.data.split(':')[1]))

    styles = await API.get_styles()
    keyboard = keyboards.styles_keyboard(styles)
    
    await callback.message.answer(texts["create_character"]["step_2"], reply_markup=keyboard)
    await state.set_state(CreateCharacterForm.waiting_for_style)


async def create_character_step_3(callback: CallbackQuery, state: FSMContext):
    await state.update_data(style=int(callback.data.split(':')[1]))
    
    data = await state.get_data()
    character = await API.create_character(
        data["name"],
        data["archetype"],
        data["style"],
        callback.from_user.id,
    )
    
    await state.clear()
    
    await callback.message.answer(texts["create_character"]["step_3"], reply_markup=keyboards.main_menu)
    await callback.message.answer("\n".join(
        (
            f"{texts["character"]["info"]["title"]}\n",
            f"{texts["character"]["info"]["name"]} {character["name"]}",
            f"{texts["character"]["info"]["archetype"]} {character["archetype"]["name"]}",
            f"{texts["character"]["info"]["style"]} {character["style"]["name"]}",
        ))
    )


async def manage_characters(message: Message, state: FSMContext):
    await state.set_state(MainForm.manage_characters)

    await message.answer(text=texts["manage_characters"]["menu"], reply_markup=keyboards.manage_characters)


async def show_all_characters(message: Message):
    characters = await API.get_characters(message.from_user.id)

    keyboard = keyboards.characters_keyboard(characters)
    
    await message.answer("Список доступных Вам персонажей", reply_markup=keyboard)
    

async def show_character(callback: CallbackQuery):
    character_id = int(callback.data.split(':')[1])
    
    character = await API.get_character(callback.from_user.id, character_id)
    
    characters = await API.get_characters(callback.from_user.id)
    keyboard = keyboards.characters_keyboard(characters)
    
    await callback.message.edit_text("\n".join(
        (
            f"{texts["character"]["info"]["title"]}\n",
            f"{texts["character"]["info"]["name"]} {character["name"]}",
            f"{texts["character"]["info"]["archetype"]} {character["archetype"]["name"]}",
            f"{texts["character"]["info"]["style"]} {character["style"]["name"]}",
        )), reply_markup=keyboard
    )


async def show_all_removable_characters(
    message: Message, state: FSMContext, user_id: Optional[int] = None
):
    user_id = user_id if user_id else message.from_user.id
    characters = await API.get_user_characters(user_id)
    
    keyboard = keyboards.remove_characters_keyboard(characters)
    
    msg = await message.answer(".", reply_markup=ReplyKeyboardRemove())
    await msg.delete()
    
    await message.answer("Список ваших персонажей", reply_markup=keyboard)
    
    await state.set_state(ManageCharactersForm.delete_characters)
    

async def ask_approve_deleting(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ManageCharactersForm.approve_deleting)
    
    character_id = int(callback.data.split(':')[1])
    
    await state.update_data(character_id=character_id)
    
    character = await API.get_character(callback.from_user.id, character_id)
        
    await callback.message.answer(
        f"""
    {texts["manage_characters"]["delete"]["approve"]} \n
    {texts["character"]["info"]["title"]}
    {texts["character"]["info"]["name"]} {character["name"]} 
    {texts["character"]["info"]["archetype"]} {character["archetype"]["name"]}
    {texts["character"]["info"]["style"]} {character["style"]["name"]}
        """, reply_markup=keyboards.remove_character_approve_keyboard
    )
    
    await callback.message.delete()
    

async def delete_character(callback: CallbackQuery, state: FSMContext):
    character_id = int((await state.get_data())["character_id"])
    
    await state.clear()
    await callback.message.delete()
    
    status = await API.delete_character(callback.from_user.id, character_id)
    
    if not status:
        await callback.message.answer(
            texts["manage_characters"]["delete"]["error"]
        )
    
    await callback.answer(
        texts["manage_characters"]["delete"]["success"]
    )
    await callback.message.answer(
        texts["manage_characters"]["delete"]["success"]
    )
    
    await manage_characters(callback.message, state)
    

async def cancel_deleting_character(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

    await show_all_removable_characters(callback.message, state, user_id=callback.from_user.id)
    

async def start_select_character(
    message: Message, state: FSMContext, user_id: Optional[int] = None
):
    user_id = user_id if user_id else message.from_user.id
    characters = await API.get_characters(user_id)
    
    await state.set_state(MainForm.select_character)
    await message.answer(
        texts["select_characters"]["start"],
        reply_markup=keyboards.select_character_keyboard(characters)
    )
    

async def ask_selecting_character(callback: CallbackQuery, state: FSMContext):
    character_id = int(callback.data.split(':')[1])
    character = await API.get_character(user_id=callback.from_user.id, character_id=character_id)
    
    await state.update_data(character_id=character_id)
    await state.set_state(SelectCharacterForm.select_character_approve)
    
    await callback.message.answer( f"""
    {texts["select_characters"]["approve"]} \n
    {texts["character"]["info"]["title"]}
    {texts["character"]["info"]["name"]} {character["name"]} 
    {texts["character"]["info"]["archetype"]} {character["archetype"]["name"]}
    {texts["character"]["info"]["style"]} {character["style"]["name"]}
        """, reply_markup=keyboards.select_character_approve_keyboard
    )
    

async def select_character(callback: CallbackQuery, state: FSMContext):
    character_id = int((await state.get_data())["character_id"])
    
    character = await API.get_character(callback.from_user.id, character_id)
    
    await callback.message.delete()
    
    msg = await callback.message.answer( f"""
    {texts["select_characters"]["finish"]} \n
    {texts["character"]["info"]["title"]}
    {texts["character"]["info"]["name"]} {character["name"]} 
    {texts["character"]["info"]["archetype"]} {character["archetype"]["name"]}
    {texts["character"]["info"]["style"]} {character["style"]["name"]}
        """, reply_markup=keyboards.exit_from_chat
    )
    await msg.pin()
    
    await state.set_state(MainForm.chat_character)
    

async def cancel_select_character(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.message.delete()

    await start_select_character(
        callback.message, state,
        user_id=callback.from_user.id
    )
