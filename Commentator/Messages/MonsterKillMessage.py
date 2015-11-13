from EventMessage import EventMessage

class MonsterKillMessage(EventMessage):
	def __init__(self, monsterId, killerId, assistIds):
		EventMessage.__init__(self, "MonsterKill")

		self.monsterId = monsterId
		self.killerId = killerId
		self.assistIds = assistIds

