
class CacheKeys:
    default_characters = "cache:characters"
    
    
    @staticmethod
    def user_characters(user_id: int):
        return f"cache:{user_id}:characters"
    
    @staticmethod
    def character(character_id: int):
        return f"{CacheKeys.default_characters}{character_id}"
    

CharacterInfoTranslation = {
    "name": "Имя",
    "archetype": "Характер",
    "style": "Стиль общения",
}
    

class CachetTTL:
    CHARACTER = 3600
    
    USER_CHARACTERS = 3600
    
    CHARACTERS = 1800