# def str_helper(seconds: float) -> str:
# 	from datetime import timedelta
# 	negative = seconds < 0
# 	seconds = abs(seconds)
# 	td = timedelta(seconds=seconds)
# 	seconds = td.seconds + 86400 * td.days
# 	microseconds = td.microseconds
# 	hours, remainder = divmod(seconds, 3600)
# 	minutes, seconds = divmod(remainder, 60)
# 	return '%s%02d:%02d:%02d.%03d' % (
# 		'-' if negative else ' ', hours, minutes,
# 		seconds, microseconds / 1000)

# Kept temporarily in case the below version doesn't work

from datetime import timedelta, datetime

def seconds_to_readable_string(seconds: float) -> str:
	"""
	Converts a number of seconds to a string in the format "HH:MM:SS.fff".

	Args:
		seconds: The number of seconds to convert.

	Returns:
		A string representation of the time.
	"""
	negative = seconds < 0
	seconds = abs(seconds)
	td = timedelta(seconds=seconds)

	# Use datetime to format the output string
	formatted_time = str(datetime.min + td)

	# Remove the leading '0' from the day and microsecond components
	formatted_time = formatted_time.replace('0 days, ', '')
	formatted_time = formatted_time[:-3]  # Remove the last three digits of microseconds

	return ('-' if negative else '') + formatted_time