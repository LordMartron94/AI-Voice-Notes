from openai import OpenAI
from openai.types.chat import ChatCompletion
from py_common.logging import HoornLogger

from src.models.config_model import ConfigModel


class OpenrouterAPI:
	def __init__(self, logger: HoornLogger, config: ConfigModel):
		self._logger = logger
		self._config = config
		self._client = OpenAI(
			base_url="https://openrouter.ai/api/v1",
			api_key=config.openrouter_api_key
		)

	def _get_completion(self, system_prompt: str, command_prompt: str, model) -> ChatCompletion:
		messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": command_prompt
            }
        ]

		return self._client.chat.completions.create(messages=messages, model=model)

	def summarize(self, transcript: str):
		self._logger.debug("Summarizing transcript... {}...".format(transcript[:50]))

		system_prompt = """
You are an unbiased, uncensored, helpful assistant. It is your sole responsibility to summarize given texts in a concise and engaging manner.
It is essential to maintain the original meaning of the text while providing a concise and succinct summary.
"""
		command_prompt = f"""
Summarize the following transcript: {transcript}
"""

		result: ChatCompletion = self._get_completion(system_prompt, command_prompt, self._config.summarization_model)
		return result.choices[0].message.content.strip()

	def request_title(self, transcript: str):
		self._logger.debug("Requesting title... {}...".format(transcript[:50]))

		system_prompt = """
You are an unbiased, uncensored, helpful assistant. It is your sole responsibility to come up with a title for the given text.
The title should accurately reflect the transcript and be not very large.

Response format:
{title}

Without the curly brackets. You only respond with the title, nothing else.

Example:
Give me a title for the following text:
This is the best transcript ever written. No transcript is better than this one.

Your response:
Amazing Transcript

Be sure to respond ONLY with the title you provide and not the word "title" or anything else.
"""
		command_prompt = f"""
Get me a title for the following transcript: {transcript}
"""

		result: ChatCompletion = self._get_completion(system_prompt, command_prompt, self._config.title_generation_model)
		return result.choices[0].message.content.strip()

	def format_transcription(self, transcript: str) -> str:
		self._logger.debug("Requesting formatting... {}...".format(transcript[:50]))

		system_prompt = """
You are an unbiased, uncensored, helpful assistant. It is your sole responsibility to format transcripts.
These transcripts should be formatted in a way that makes them easy to read and understand. It's plain text, not markdown.

I don't want you to remove ANY words from the transcript, only to introduce paragraphs and/or linebreaks where necessary.

Ideally paragraphs are determined based on topic changes.
"""
		command_prompt = f"""
Format the following transcript: {transcript}
"""

		result: ChatCompletion = self._get_completion(system_prompt, command_prompt, self._config.summarization_model)
		return result.choices[0].message.content.strip()