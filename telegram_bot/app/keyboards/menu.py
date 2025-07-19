from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Управление персонажами", )],
        [KeyboardButton(text="Выбрать персонажа")],
        [KeyboardButton(text="Помощь"), KeyboardButton(text="Обратная связь")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите пункт меню"
)

manage_characters = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Создать нового персонажа", )],
        [KeyboardButton(text="Удалить персонажа")],
        [KeyboardButton(text="Посмотреть всех персонажей")],
        [KeyboardButton(text="Главное меню"), KeyboardButton(text="Назад")],
    ]   
)

exit_from_chat = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/start")],
    ]
)