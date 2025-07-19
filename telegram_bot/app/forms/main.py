from aiogram.fsm.state import State, StatesGroup


class MainForm(StatesGroup):
    waiting_for_command = State()
    
    manage_characters = State()

    select_character = State()
    chat_character = State()