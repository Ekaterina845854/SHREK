

from typing import Optional
from app.utils.constants import CharacterInfoTranslation


def get_character_creating_info(data: Optional[dict] = None):
    info = {
        "Имя": '-',
        "Характер": '-',
        "Стиль общения": '-',
    }
    
    if data:
        for key, value in data.items():
            info[CharacterInfoTranslation[key]] = value
    
    return info
    
    