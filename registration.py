from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

router = Router()

class Registration(StatesGroup):
    name = State()
    surname = State()
    phone = State()

@router.message(F.text.lower() == "ro'yxatdan o'tish")
async def start_register(message: Message, state: FSMContext):
    await message.answer("Ismingizni kiriting:")
    await state.set_state(Registration.name)

@router.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Familiyangizni kiriting:")
    await state.set_state(Registration.surname)

@router.message(Registration.surname)
async def process_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)

    # Telefon raqam uchun tugma
    contact_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Raqamni yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

    await message.answer("Telefon  raqamingizni yuboring:", reply_markup=contact_keyboard)
    await state.set_state(Registration.phone)

@router.message(Registration.phone, F.contact)
async def process_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    data = await state.get_data()

    await message.answer(
        f"✅ Tabriklaymiz siz konkursda ro'yxatdan o'tdingiz!\n\n",
        reply_markup=None
    )
    await state.clear()
