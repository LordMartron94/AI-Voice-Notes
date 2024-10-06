from typing import Any

from py_common.logging import HoornLogger
from py_common.patterns.pipeline.pipe import IPipe

from src.models.config_model import ConfigModel
from src.summarization.openrouter_api import OpenrouterAPI


class Summarize(IPipe):
	def __init__(self, config_model: ConfigModel, logger: HoornLogger):
		self._config_model = config_model
		self._logger = logger
		self._openrouter_api: OpenrouterAPI = OpenrouterAPI(logger, config_model)

	def flow(self, data: Any) -> Any:
		self._logger.info("Start summarizing audio data.")
		data: list[str] = data

		output: list[tuple[str, str, str]] = []

		for transcript in data:
			summary = self._openrouter_api.summarize(transcript)
			title = self._openrouter_api.request_title(transcript)
			self._logger.debug(f"Summarized: {summary}")
			output.append((transcript, summary, title))

		return output
