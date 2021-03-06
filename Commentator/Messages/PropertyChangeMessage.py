from EventMessage import EventMessage

class PropertyChangeMessage(EventMessage):
	def __init__(self, propertyName, sourceId, value):
		EventMessage.__init__(self, "Update")

		self.propertyName = propertyName
		self.sourceId = sourceId
		self.value = value
