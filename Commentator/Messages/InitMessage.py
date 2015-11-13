from EventMessage import EventMessage;

class InitMessage(EventMessage):
	def __init__(self, summonerNames, championNames):
		EventMessage.__init__(self, "Init");

		self.summonerNames = summonerNames;
		self.championNames = championNames;

