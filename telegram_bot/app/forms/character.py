from aiogram.fsm.state import State, StatesGroup


class CreateCharacterForm(StatesGroup):
    waiting_for_name = State()
    waiting_for_archetype = State()
    waiting_for_style = State()


class ManageCharactersForm(StatesGroup):
    delete_characters = State()
    approve_deleting = State()
    

class SelectCharacterForm(StatesGroup):
    select_character_approve = State()