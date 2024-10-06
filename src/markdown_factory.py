from py_common.logging import HoornLogger


class MarkdownFactory:
	def __init__(self, logger: HoornLogger):
		self._logger = logger

	def create_heading(self, level: int, content: str) -> str:
		if level < 1 or level > 6:
			self._logger.error(f"Invalid heading level: {level}. Must be between 1 and 6.")
			return content

		return f"{'#' * level} {content}"
