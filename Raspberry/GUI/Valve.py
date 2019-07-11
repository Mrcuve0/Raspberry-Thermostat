class Valve(object):

    ID = 0

    def __init__(self, isUsed):
        self.ID = self.ID + 1
        self.isUsed = isUsed
        
    ### SETTERS ### 

    def setIsUsed(self, isUsed):
        self.isUsed = isUsed

    ### GETTERS ###

    def getID(self):
        return self.ID

    def getIsUsed(self):
        return self.isUsed