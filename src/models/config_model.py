import json
from pathlib import Path

import pydantic


class ConfigModel(pydantic.BaseModel):
	audio_input_directory: Path
	note_output_directory: Path
	delete_audio: bool
	hugging_face_authorization_token: str
	used_whisper_model: str
	language: str
	openrouter_api_key: str
	summarization_model: str
	title_generation_model: str
	formatting_cue_words: list[str]
	formatting_pause_threshold: float

	@classmethod
	def from_json(cls, json_file: Path) -> "ConfigModel":
		with open(str(json_file), "r") as file:
			data = json.load(file)
			return cls(**data)