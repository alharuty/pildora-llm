from cog import BasePredictor, Input
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

SYSTEM_PROMPT = (
    "Eres un experto en limpieza del hogar con años de experiencia ayudando a personas a mantener sus casas limpias, "
    "ordenadas y libres de suciedad. Puedes dar consejos detallados sobre cómo limpiar cualquier parte de una casa, "
    "desde superficies hasta ropa, explicando métodos, productos recomendados y precauciones. "
    "Si la pregunta no está relacionada con limpieza del hogar, responde amablemente que solo puedes ayudar con limpieza."
)

class Predictor(BasePredictor):
    def setup(self):
        model_name = "tiiuae/falcon-rw-1b"
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32,
            device_map="auto"
        )
        self.model.eval()

    def predict(self, pregunta: str = Input(description="Pregunta relacionada con limpieza del hogar")) -> str:
        prompt = f"{SYSTEM_PROMPT}\n\nUsuario: {pregunta}\nRespuesta:"
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=256,
            do_sample=True,
            temperature=0.7,
            pad_token_id=self.tokenizer.eos_token_id
        )
        respuesta = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        # Extraemos la respuesta eliminando el prompt
        respuesta = respuesta[len(prompt):].strip()
        return respuesta
