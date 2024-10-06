from pathlib import Path
from typing import List

from py_common.logging import HoornLogger, HoornLogOutputInterface, DefaultHoornLogOutput, FileHoornLogOutput, LogType

from src.models.config_model import ConfigModel
from src.processing_pipeline.processing_pipeline import ProcessingPipeline


def get_user_local_app_data_dir() -> Path:
	return Path.home() / "AppData" / "Local"

def get_user_log_directory() -> Path:
	return get_user_local_app_data_dir() / "AI Voice Notes/Logs"


if __name__ == "__main__":
	log_dir = get_user_log_directory()

	outputs: List[HoornLogOutputInterface] = [
		DefaultHoornLogOutput(),
		FileHoornLogOutput(log_dir, 5, True)
	]

	logger: HoornLogger = HoornLogger(
		outputs,
		min_level=LogType.DEBUG,
	)

	config_model: ConfigModel = ConfigModel.from_json(Path("config\\main_config.json"))

	logger.info("Processing started")
	pipeline: ProcessingPipeline = ProcessingPipeline(config_model, logger)
	pipeline.build_pipeline()
	pipeline.flow(None)
	logger.info("Processing completed")
