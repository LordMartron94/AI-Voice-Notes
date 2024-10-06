from pathlib import Path
from typing import Any, List

from py_common.logging import HoornLogger
from py_common.patterns.pipeline.pipe import IPipe
from stable_whisper import WhisperResult

from src.models.config_model import ConfigModel
from src.transcription.whisper_api import WhisperAPI


class Transcribe(IPipe):
	def __init__(self, config_model: ConfigModel, logger: HoornLogger):
		self._config_model = config_model
		self._logger = logger
		self._whisper_api: WhisperAPI = WhisperAPI(config_model, logger)

	def _transcribe_audio_file(self, audio_file: Path) -> WhisperResult:
		return self._whisper_api.get_transcription_for_audio(audio_file, language=self._config_model.language)

	def flow(self, data: Any) -> Any:
		self._logger.info("Start transcribing audio files.")
		audio_files: List[Path] = data

		data: list[WhisperResult] = []

		for audio_file in audio_files:
			transcription = self._transcribe_audio_file(audio_file)
			data.append(transcription)

			if self._config_model.delete_audio:
				audio_file.unlink()

		return data