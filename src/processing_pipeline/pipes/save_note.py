import re
from typing import Any

from py_common.logging import HoornLogger
from py_common.patterns.pipeline.pipe import IPipe

from src.markdown_factory import MarkdownFactory
from src.models.config_model import ConfigModel


class SaveNote(IPipe):
	def __init__(self, config_model: ConfigModel, logger: HoornLogger):
		self._config_model = config_model
		self._logger = logger
		self._factory: MarkdownFactory = MarkdownFactory(logger)

	def _convert_to_markdown(self, transcript: str, summary: str, title: str) -> str:
		title_heading = self._factory.create_heading(1, title)
		transcript_heading = self._factory.create_heading(2, "Transcript")
		summary_heading = self._factory.create_heading(2, "Summary")

		return f"""{title_heading}

{summary_heading}
{summary}

{transcript_heading}
{transcript}
"""

	def _save_to_file(self, markdown_note: str, title: str) -> None:
		note_file_path = self._config_model.note_output_directory / f"{title}.md"
		with open(note_file_path, "w", encoding="utf-8") as file:
			file.write(markdown_note)
			self._logger.info(f"Saved note to {note_file_path}")

	def _get_normalized_title(self, title: str) -> str:
		normalized_title = re.sub(r'[\\/:*?"<>|]', ' ', title)
		normalized_title = normalized_title.strip()
		return normalized_title

	def flow(self, data: Any) -> Any:
		self._logger.info(f"Saving notes...")
		transcriptions: list[tuple[str, str, str]] = data # tuple [ transcript, summary, title ]

		for transcript, summary, title in transcriptions:
			markdown_note = self._convert_to_markdown(transcript, summary, title)
			self._save_to_file(markdown_note, self._get_normalized_title(title))
