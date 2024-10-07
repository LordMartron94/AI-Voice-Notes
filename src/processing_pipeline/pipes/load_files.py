from typing import Any

from py_common.handlers import FileHandler
from py_common.logging import HoornLogger
from py_common.patterns.pipeline.pipe import IPipe

from src.models.config_model import ConfigModel


class LoadFiles(IPipe):
	def __init__(self, config_model: ConfigModel, logger: HoornLogger):
		self._config_model = config_model
		self._logger = logger
		self._filehandler: FileHandler = FileHandler()
		self._supported = [".mp3", ".wav", ".ogg", ".opus", ".m4a"]

	def _get_audio_files(self) -> list:
		all_audio_files = []

		for extension in self._supported:
			all_audio_files.extend(self._filehandler.get_children_paths(self._config_model.audio_input_directory, extension))

		return all_audio_files

	def flow(self, data: Any) -> Any:
		self._logger.debug("LoadFiles: Loading audio files from specified directory.")
		audio_files = self._get_audio_files()
		self._logger.info(f"LoadFiles: Found {len(audio_files)} audio files.")
		return audio_files