import os

from openai import OpenAI


class AIRunner:
	def __init__(self):
		self.client = OpenAI(
			base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1"),
			api_key="ollama",
			timeout=180.0,
		)
		self.model = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b")
		self.review_model = os.getenv("OLLAMA_REVIEW_MODEL", self.model)

	def call(self, system_prompt: str, user_prompt: str, review: bool = False) -> tuple[str | None, str | None]:
		try:
			response = self.client.chat.completions.create(
				model=self.review_model if review else self.model,
				messages=[
					{"role": "system", "content": system_prompt},
					{"role": "user", "content": user_prompt},
				],
				max_tokens=180,
				temperature=0.1,
			)
			content = response.choices[0].message.content
			return (content.strip() if content else "No response generated."), None
		except Exception as exc:
			return None, str(exc)
