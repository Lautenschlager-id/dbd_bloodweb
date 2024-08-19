from concurrent.futures import ProcessPoolExecutor, as_completed
from sys import exit

from utils.logger import logger

def multithreaded_execute(callback, **kwargs):
	should_exit = False

	with ProcessPoolExecutor() as executor:
		futures = []

		callback(executor, futures, **kwargs)

		for future in as_completed(futures):
			try:
				result = future.result()
			except Exception as exception:
				logger.result(
					'Threaded task generated an exception: {}'
					, exception
				)
				should_exit = True

	if should_exit:
		exit()
