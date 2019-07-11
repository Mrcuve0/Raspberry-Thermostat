class Sensor(object):

    ID = 0

    def __init__(self, isConnected):
        self.ID = self.ID + 1
        self.isConnected = isConnected

    ### SETTERS ###

    def setIsConnect(self, isConnected):
        self.isConnected = isConnected

    ### GETTERS ###

    def getID(self):
        return self.ID

    def getIsConnected(self):
        return self.isConnected

