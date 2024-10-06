import tempfile
from pathlib import Path

import librosa
import stable_whisper
import torch
from py_common.logging import HoornLogger
from pyannote.audio import Pipeline
from stable_whisper import WhisperResult

import soundfile as sf

from src.models.config_model import ConfigModel
from src.utils import seconds_to_readable_string


class WhisperAPI:
	def __init__(self, config: ConfigModel, logger: HoornLogger):
		self._logger = logger
		self._config = config
		self.vad_pipeline: Pipeline = Pipeline.from_pretrained("pyannote/voice-activity-detection", use_auth_token=config.hugging_face_authorization_token)

		# Switch to CUDA if available
		if torch.cuda.is_available():
			device = torch.device('cuda')  # Create a torch.device object for CUDA
		else:
			device = torch.device('cpu')   # Fallback to CPU

		self.vad_pipeline.to(device)

	def _get_model(self):
		try:
			return stable_whisper.load_model(self._config.used_whisper_model, device="cuda")
		except RuntimeError:  # If the model is already loaded, reuse it.
			return stable_whisper.load_model(self._config.used_whisper_model, device="cuda", in_memory=False)

	def _get_segments_sorted(self, audio, sampling_rate) -> list:
		with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio_file:
			sf.write(temp_audio_file.name, audio, sampling_rate)
			temp_audio_path = temp_audio_file.name

		vad_result = self.vad_pipeline(temp_audio_path)

		Path(temp_audio_path).unlink()

		return sorted(vad_result.itersegments(), key=lambda seg: seg.start)

	def _process_segment(self, model, audio, sampling_rate, segment, language):
		start, end = segment.start, segment.end

		self._logger.info(f"Processing segment from {seconds_to_readable_string(start)} to {seconds_to_readable_string(end)}")

		segment_audio = audio[int(start * sampling_rate):int(end * sampling_rate)]

		if language is None:
			segment_result = model.transcribe(segment_audio, verbose=True, task="transcribe", temperature=0.1, word_timestamps=True)
		else:
			segment_result = model.transcribe(segment_audio, verbose=True, task="transcribe", temperature=0.1, word_timestamps=True, language=language)

		if hasattr(segment_result, 'word_timestamps'):
			adjusted_text = ""
			for word_data in segment_result.word_timestamps:
				adjusted_text += f"{word_data[0].strip()} "
		else:
			adjusted_text = segment_result.text.strip()

		segment_data = {
			"text": adjusted_text,
			"start": segment.start,
			"end": segment.end
		}

		return segment_data

	def get_transcription_for_audio(self, audio_path: Path, language=None) -> WhisperResult:
		model = self._get_model()
		audio, sampling_rate = librosa.load(audio_path)
		sorted_segments: list = self._get_segments_sorted(audio, sampling_rate)

		# Transcribe each combined segment
		segments_data = []
		for segment in sorted_segments:
			segments_data.append(self._process_segment(model, audio, sampling_rate, segment, language))

		# Create the WhisperResult object with the structured data
		result_data = {
			"segments": segments_data,
			"language": "en" if language is None else language
		}

		result = WhisperResult(result=result_data)
		return result
