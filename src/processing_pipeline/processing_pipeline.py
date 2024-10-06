from py_common.logging import HoornLogger
from py_common.patterns.pipeline.abstract_pipeline import AbPipeline

from src.models.config_model import ConfigModel
from src.processing_pipeline.pipes.format_transcripts import FormatTranscripts
from src.processing_pipeline.pipes.load_files import LoadFiles
from src.processing_pipeline.pipes.save_note import SaveNote
from src.processing_pipeline.pipes.summarize import Summarize
from src.processing_pipeline.pipes.transcribe import Transcribe


class ProcessingPipeline(AbPipeline):
	def __init__(self, config: ConfigModel, logger: HoornLogger):
		self._config = config
		self._logger = logger
		super().__init__()

	def build_pipeline(self):
		self._add_step(LoadFiles(self._config, self._logger))
		self._add_step(Transcribe(self._config, self._logger))
		self._add_step(FormatTranscripts(self._config, self._logger))
		self._add_step(Summarize(self._config, self._logger))
		self._add_step(SaveNote(self._config, self._logger))
