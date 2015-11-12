from EventMessage import EventMessage

class PropertyChangeMessage(EventMessage):
	def __init__(self, eventName, propertyName, sourceId, value):
		EventMessage.__init__(self, eventName);

		self.propertyName = propertyName;
		self.sourceId = sourceId;
		self.value = value;
