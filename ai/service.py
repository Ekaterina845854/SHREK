from app.src.dependency.constants import ARCHETYPES, EMOJI_EXAMPLES, TONE_TYPES
from pathlib import Path
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
)

class LoraModelForCausalLM(AutoModelForCausalLM):
    def __init__(self, path_to_model: str, use_emoji: bool = False):
        MODEL_PATH = Path(path_to_model).resolve()
        
        self.model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, local_files_only=True)
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
        self.model.eval()
        
        self.use_emoji = use_emoji


    def generate_response(self, input_text: str, archetype: str, style: str) -> str:
        style = style.lower()
        reply = self._generate_response(
            prompt=input_text,
            archetype=archetype,
            use_emoji=self.use_emoji,
            tone=style
        )
        
        return reply

    def _generate_response(
        self,
        prompt,
        archetype="Романтик",
        use_emoji=True,
        tone="добрый",
        max_new_tokens=100
    ):
        emoji_str = "да" if use_emoji else "нет"
        instruction = f"""
    [Архетип: {archetype}]
    [Смайлики: {emoji_str}]
    [Тон: {tone}]
    [Инструкция: отвечай как {archetype}, используя стиль: {ARCHETYPES[archetype]['description']}, примеры: {', '.join(ARCHETYPES[archetype]['example_phrases'])}, тон: {TONE_TYPES[tone]}]

    User: {prompt}
    {archetype}:"""

        inputs = self.tokenizer(instruction, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.75,
            top_p=0.9,
            top_k=50,
            repetition_penalty=1.2,
            pad_token_id=self.tokenizer.eos_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )

        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)

        if archetype + ":" in response:
            response = response.split(archetype + ":")[-1].strip()

        if use_emoji and archetype in EMOJI_EXAMPLES:
            response += " " + " ".join(EMOJI_EXAMPLES[archetype][:2])

        return response
    
model: LoraModelForCausalLM = None