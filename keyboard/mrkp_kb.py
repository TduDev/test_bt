from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, KeyboardButtonPollType
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# Клавиатура под экраном
new_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='menu'),
            KeyboardButton(text='about'),
        ],
        [
            KeyboardButton(text='payment'),
            KeyboardButton(text='delivery')
        ],
        [
            KeyboardButton(text='pos')
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='Choose your option'
)

# Удаление клавиатуры
del_key = ReplyKeyboardRemove

# Другой варинат создания клавиатуры
bilder_kd = ReplyKeyboardBuilder()
bilder_kd.add(
    KeyboardButton(text='menu'),
    KeyboardButton(text='about'),
    KeyboardButton(text='payment'),
    KeyboardButton(text='delivery'),
    KeyboardButton(text='pos')
)

bilder_kd.adjust(2, 1, 2)

# Создание клавиатуры на основе другой клавиатуры и добавление еще одной кнопки.
kb2 = ReplyKeyboardBuilder()
kb2.attach(bilder_kd)
kb2.row(KeyboardButton(text='Отзыв'))

# Создание клавиатуры с опросом KeyboardButtonPollType()
reviev_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Опрос', request_poll=KeyboardButtonPollType())
        ],
        [
            KeyboardButton(text='Контакт 🖋', request_contact=True),
            KeyboardButton(text='Локация 📧', request_location=True)
        ]
    ],
    resize_keyboard=True,
    input_field_placeholder='оставить отзыв'

)
