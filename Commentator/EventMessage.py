
class EventMessage(object):
	def __init__(self, propertyName, sourceId, value):
		self.propertyName = propertyName;
		self.sourceId = sourceId;
		self.value = value;
