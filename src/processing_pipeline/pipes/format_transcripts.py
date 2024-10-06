import re
import string
from typing import Any

import nltk
from py_common.logging import HoornLogger
from py_common.patterns import IPipe
from stable_whisper import WhisperResult

from src.models.config_model import ConfigModel
from src.summarization.openrouter_api import OpenrouterAPI


class FormatTranscripts(IPipe):
	def __init__(self, config_model: ConfigModel, logger: HoornLogger):
		self._config_model = config_model
		self._logger = logger
		self._openrouter_api: OpenrouterAPI = OpenrouterAPI(logger, config_model)

	# def _clean_sentence(self, sentence):
	# 	# Remove repeated filler words (keep one if repeated)
	# 	sentence = re.sub(r'\b(uh|um|like)\b\s+\1\b', r'\1', sentence, flags=re.IGNORECASE)
	# 	sentence = re.sub(r'\s+', ' ', sentence)  # Normalize whitespace
	# 	return sentence
	#
	# def _format_sentence(self, sentence):
	# 	if sentence:
	# 		sentence = sentence.capitalize()
	# 		if sentence[-1] not in string.punctuation:
	# 			sentence += "."
	# 	return sentence
	#
	# def _format_transcript(self, transcript: WhisperResult) -> str:
	# 	sentences = []
	# 	timestamps = []
	#
	# 	for segment in transcript.segments:
	# 		sentences.append(segment.text)
	# 		timestamps.append(segment.start)
	#
	# 	cleaned_sentences = [self._clean_sentence(sentence) for sentence in sentences]
	# 	formatted_sentences = [self._format_sentence(sentence) for sentence in cleaned_sentences]
	#
	# 	paragraphs = []
	# 	current_paragraph = ""
	# 	pause_threshold = self._config_model.formatting_pause_threshold
	#
	# 	for i, sentence in enumerate(formatted_sentences):
	# 		if any(cue_word in sentence.lower() for cue_word in self._config_model.formatting_cue_words):
	# 			paragraphs.append(current_paragraph.strip())
	# 			current_paragraph = ""
	#
	# 		current_paragraph += sentence + " "
	#
	# 		# Pause-based paragraphing
	# 		if i < len(formatted_sentences) - 1 and timestamps[i + 1] - timestamps[i] > pause_threshold:
	# 			paragraphs.append(current_paragraph.strip())
	# 			current_paragraph = ""
	#
	# 	paragraphs.append(current_paragraph.strip())
	# 	return "\n\n".join(paragraphs)

# Kept only because we might revert to it if transcripts become large (and thus costly)

	def flow(self, data: Any) -> Any:
		self._logger.info("Formatting transcripts")

		transcripts: list[WhisperResult] = data
		output = []

		for transcript in transcripts:
			output.append(self._openrouter_api.format_transcription(transcript.text))

		return output