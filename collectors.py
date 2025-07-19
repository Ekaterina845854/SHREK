from dataclasses import dataclass
from typing import List, Dict, Optional
import json
from dataclasses import asdict


@dataclass
class CharacterDataset:
    """Структура датасета для обучения персонажа по новому ТЗ"""

    character_name: str
    role_and_purpose: str
    format: str
    target_audience: str
    language: str

    personality_type: str
    key_traits: List[str]
    tone_of_communication: str
    initiative_level: str
    attitude_towards_user: str

    language_register: str
    language_complexity: str
    uses_emoji: str
    emoji_examples: List[str]
    uses_memes: str
    memes_examples: List[str]
    uses_stickers: str
    example_phrases: List[str]

    core_tasks: List[str]
    context_memory: str
    scenarios: List[str]

    visual_type: str
    age_and_gender: str
    clothing_style: str
    color_palette: str
    signature_gestures: str
    avatar_or_stickerpack: str

    integrations: List[str]
    ai_component: str
    ui_buttons: str
    timeouts_logic: str
    platforms: List[str]

    content_filter: str
    banned_topics: List[str]
    moderation_triggers: List[str]
    behavior_restrictions: str

    scalability: str
    brand_tone_guidelines: str
    references: List[str]

    # Диалоги
    dialogues: List[Dict[str, str]]

class DatasetCollector:
    """Сборщик данных для персонажа из фильма"""

    def __init__(self):
        self.all_dialogs = []
    def load_dialogues_from_json(self, json_path: str):
        """Загружает диалоги из JSON и проверяет их структуру"""
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError as e:
                raise ValueError(f"Ошибка чтения JSON: {e}")

        # Проверяем и сохраняем только корректные записи
        self.all_dialogs = []
        for item in data:
            if isinstance(item, dict) and "character_name" in item and "line" in item:
                self.all_dialogs.append({
                    "character": item["character_name"],
                    "line": item["line"]
                })
            else:
                print(f"[Предупреждение] Пропущена некорректная запись: {item}")

    def _build_context_response_pairs(self, character: str) -> List[Dict[str, str]]:
        """
        Создаёт пары (контекст, реплика персонажа)
        :param character: имя персонажа, для которого строим датасет
        :return: список пар, где response — реплика персонажа
        """
        pairs = []

        for i in range(len(self.all_dialogs)):
            current = self.all_dialogs[i]

            if current["character"] == character:
                if i > 0:
                    context = self.all_dialogs[i - 1]["line"]
                    response = current["line"]
                    pairs.append({
                        "context": context,
                        "response": response
                    })
        return pairs

    def create_dataset_manually(
        self,
        character: str,
        role_and_purpose: str,
        format: str,
        target_audience: str,
        language: str,
        personality_type: str,
        key_traits: List[str],
        tone_of_communication: str,
        initiative_level: str,
        attitude_towards_user: str,
        language_register: str,
        language_complexity: str,
        uses_emoji: str,
        emoji_examples: List[str],
        uses_memes: str,
        memes_examples: List[str],
        uses_stickers: str,
        example_phrases: List[str],
        core_tasks: List[str],
        context_memory: str,
        scenarios: List[str],
        visual_type: str,
        age_and_gender: str,
        clothing_style: str,
        color_palette: str,
        signature_gestures: str,
        avatar_or_stickerpack: str,
        integrations: List[str],
        ai_component: str,
        ui_buttons: str,
        timeouts_logic: str,
        platforms: List[str],
        content_filter: str,
        banned_topics: List[str],
        moderation_triggers: List[str],
        behavior_restrictions: str,
        scalability: str,
        brand_tone_guidelines: str,
        references: List[str],
    ) -> Optional[CharacterDataset]:
        """Создаёт CharacterDataset с заданными параметрами и диалогами из JSON"""

        if not any(item["character"] == character for item in self.all_dialogs):
            print(f"Персонаж {character} не найден в датасете.")
            return None

        dialogues = self._build_context_response_pairs(character)

        return CharacterDataset(
            character_name=character,
            role_and_purpose=role_and_purpose,
            format=format,
            target_audience=target_audience,
            language=language,

            personality_type=personality_type,
            key_traits=key_traits,
            tone_of_communication=tone_of_communication,
            initiative_level=initiative_level,
            attitude_towards_user=attitude_towards_user,

            language_register=language_register,
            language_complexity=language_complexity,
            uses_emoji=uses_emoji,
            emoji_examples=emoji_examples,
            uses_memes=uses_memes,
            memes_examples=memes_examples,
            uses_stickers=uses_stickers,
            example_phrases=example_phrases,

            core_tasks=core_tasks,
            context_memory=context_memory,
            scenarios=scenarios,

            visual_type=visual_type,
            age_and_gender=age_and_gender,
            clothing_style=clothing_style,
            color_palette=color_palette,
            signature_gestures=signature_gestures,
            avatar_or_stickerpack=avatar_or_stickerpack,

            integrations=integrations,
            ai_component=ai_component,
            ui_buttons=ui_buttons,
            timeouts_logic=timeouts_logic,
            platforms=platforms,

            content_filter=content_filter,
            banned_topics=banned_topics,
            moderation_triggers=moderation_triggers,
            behavior_restrictions=behavior_restrictions,

            scalability=scalability,
            brand_tone_guidelines=brand_tone_guidelines,
            references=references,

            dialogues=dialogues
        )


# === Пример использования: Шрек ===
if __name__ == "__main__":
    collector = DatasetCollector()
    collector.load_dialogues_from_json("movie_dialogues.json")

    character_dataset = collector.create_dataset_manually(
        character="Donkey",
        role_and_purpose="Funny, kind and extravert. Loves his friends",
        format="Чат-бот в Telegram",
        target_audience="18-30 лет, любители юмора и фэнтези",
        language="русский",

        personality_type="Kind, loveful",
        key_traits=["kinf", "самостоятельный", "clever", "strong"],
        tone_of_communication="дружелюбный",
        initiative_level="средний",
        attitude_towards_user="support",

        language_register="informal",
        language_complexity="simple",
        uses_emoji="not a lot",
        emoji_examples=["😎", "💡", "🧠", "🐸"],
        uses_memes="по ситуации",
        memes_examples=["Когда ты не сдал дз", "Бу! Испугался? Не бойся"],
        uses_stickers="нет",
        example_phrases=[
            "Жизнь — как коробка шоколадных конфет…",
            "Ты мне нравишься, когда злишься.",
        ],

        core_tasks=[
            "Поддерживать беседу",
            "Отвечать на вопросы",
            "Участвовать в обучении и тренировке"
        ],
        context_memory="имя, уровень, предыдущие диалоги",
        scenarios=[
            "onboarding",
            "реакция на эмоции пользователя",
            "юмористические ремарки"
        ],

        visual_type="2D",
        age_and_gender="взрослый мужчина",
        clothing_style="зелёный плащ и доспехи",
        color_palette="зелёно-коричневые тона",
        signature_gestures="подмигивание, ухмылка",
        avatar_or_stickerpack="Midjourney",

        integrations=["Telegram Bot API", "GPT"],
        ai_component="GPT, температура 0.7",
        ui_buttons="Reply",
        timeouts_logic="случайные задержки 0.5–2 секунды",
        platforms=["Telegram"],

        content_filter="да",
        banned_topics=["politics", "religion", "fight"],
        moderation_triggers=["ругательства", "провокации"],
        behavior_restrictions="не должен поддерживать романтические или личные связи",

        scalability="да, можно добавлять новые функции и визуал",
        brand_tone_guidelines="дружелюбный, но с характером",
        references=["@replika_bot", "@dotline_bot", "Persona X из [название проекта]"],
    )

    if character_dataset:
        # Сохраняем в JSON
        output_path = "Donkey_dataset.json"
        dataset_dict = asdict(character_dataset)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(dataset_dict, f, ensure_ascii=False, indent=4)

        print(f"Датасет успешно сохранён в {output_path}")
    else:
        print("Не удалось создать датасет.")