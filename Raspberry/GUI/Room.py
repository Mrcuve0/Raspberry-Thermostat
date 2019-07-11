from Sensor import Sensor
from Actuator import Actuator

class Room(object):

    ID = 0

    def __init__(self):
        self.ID = self.ID + 1

        # Dizionario di sensori connessi a questa stanza
        self.sensorsDict = {}   

        # Dizionario di attuatori connessi a questa stanza
        self.actuatorsDict = {}

    ### SETTERS ###

    def addActuator(self):
        act = Actuator()
        self.actuatorsDict[act.getID()] = act

    def addSensor(self, isConnected):
        sens = Sensor(isConnected)
        self.sensorsDict[sens.getID()] = sens

    ### GETTERS ###

    def getSensorsConnected(self):
        return self.sensorsDict

    def getActuatorsConnected(self):
        return self.actuatorsDict


    

