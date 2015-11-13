from EventMessage import EventMessage;

class KillMessage(EventMessage):
	def __init__(self, victimId, killerId, assistIds):
		EventMessage.__init__(self, "Init");

		self.victimId = victimId;
		self.killerId = killerId;
		self.assistIds = assistIds;

