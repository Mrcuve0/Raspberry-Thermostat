from Valve import Valve

class Actuator(object):
    
    ID = 0

    def __init__(self):
        self.ID = self.ID + 1

        # Dizionario di valvole connesse a questo sensore
        self.valvesDict = {}
        

    ### SETTERS ###

    def addValve(self, isConnected):
        valve = Valve(isConnected)
        self.valvesDict[valve.getID] = valve

    ### GETTERS ###

    def getID(self):
        return self.ID

    def getValvesConnected(self):
        return self.valvesDict

    