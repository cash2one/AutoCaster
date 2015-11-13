from EventMessage import EventMessage;

class InitMessage(EventMessage):
	def __init__(self, summonerNames, championNames, dataIds):
		EventMessage.__init__(self, "Init");

		self.summonerNames = summonerNames;
		self.championNames = championNames;
		self.dataIds = dataIds;

