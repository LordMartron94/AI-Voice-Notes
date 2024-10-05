import json
from pathlib import Path

import pydantic


class ConfigModel(pydantic.BaseModel):
	audio_input_directory: Path
	note_output_directory: Path
	delete_audio: bool

	@classmethod
	def from_json(cls, json_file: Path) -> "ConfigModel":
		with open(str(json_file), "r") as file:
			data = json.load(file)
			return cls(**data)