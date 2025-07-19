import asyncio

from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from app.forms import MainForm
from app.utils.api import API
from app.utils.texts import texts


async def create_task(message: Message, state: FSMContext):
    task_id = (await state.get_data()).get("task_id", None)
    
    if task_id:
        return await message.answer(texts["create_task"]["already_exists"])
    
    msg = await message.answer(texts["create_task"]["step_0"])
    
    character_id = (await state.get_data())["character_id"]
    
    try:
        await state.update_data(task_id="wait")
        task_id = await API.ask_character(message.from_user.id, character_id, message.text)
        await state.update_data(task_id=task_id)
    except Exception as e:
        await state.update_data(task_id=None)
        return await message.answer("Произошла ошибка при генерации ответа.")
    
    await _check_task(msg, state, task_id)
    

async def _check_task(message: Message, state: FSMContext, task_id: str):
    for _ in range(60):
        await asyncio.sleep(1)

        try:
            response = await API.check_task(task_id)
            
            if response is False:
                await state.update_data(task_id=None)
                return await message.answer("Произошла ошибка при генерации ответа.")
            
            if response is None:
                continue
            
            await state.update_data(task_id=None)
            await state.set_state(MainForm.chat_character)
            
            await message.delete()
            return await message.answer(response)      
        except Exception:
            continue
    
    await state.update_data(task_id=None)
    return await message.answer("Произошла ошибка при генерации ответа.")