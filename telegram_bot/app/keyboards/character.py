from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder


def archetypes_keyboard(archetypes: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for archetype in archetypes:
        builder.button(
            text=archetype["name"],
            callback_data=f"archetype:{archetype["archetype_id"]}"
        )

    builder.adjust(2)
    
    return builder.as_markup()


def styles_keyboard(styles: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for style in styles:
        builder.button(
            text=style["name"],
            callback_data=f"style:{style["style_id"]}"
        )

    builder.adjust(2)
    
    return builder.as_markup()


def characters_keyboard(characters: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for character in characters:
        builder.button(
            text=character["name"],
            callback_data=f"show_character:{character["character_id"]}"
        )

    builder.adjust(2)
    
    return builder.as_markup()


def remove_characters_keyboard(characters: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for character in characters:
        builder.button(
            text=character["name"],
            callback_data=f"delete_character:{character["character_id"]}"
        )

    builder.adjust(2)
    
    return builder.as_markup()


def select_character_keyboard(characters: list[dict]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    
    for character in characters:
        builder.button(
            text=character["name"],
            callback_data=f"select_character:{character["character_id"]}"
        )

    builder.adjust(2)
    
    return builder.as_markup()


remove_character_approve_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Удалить", callback_data="delete_character:approve")],
        [InlineKeyboardButton(text="Отмена", callback_data="delete_character:cancel")],
    ]
)

select_character_approve_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выбрать", callback_data="select_character:approve")],
        [InlineKeyboardButton(text="Отмена", callback_data="select_character:cancel")],
    ]
)