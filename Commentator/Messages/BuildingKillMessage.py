from EventMessage import EventMessage

class BuildingKillMessage(EventMessage):
	def __init__(self, buildingId, killerId, assistIds):
		EventMessage.__init__(self, "BuildingKill")

		self.buildingId = buildingId
		self.killerId = killerId
		self.assistIds = assistIds

