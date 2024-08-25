class FilenamePattern:
	def __init__(self, entry):
		self.identifier = None
		self.threshold = None

		self.pattern = None

		if isinstance(entry, list):
			self.identifier = entry[0]
			self.threshold = entry[1]
		else:
			self.identifier = entry