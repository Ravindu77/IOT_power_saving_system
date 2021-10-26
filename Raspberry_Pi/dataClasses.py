class Reading:
    def __init__(self, date, temp, humid):
        self.date = date
        self.temp = temp
        self.humid = humid

class Power:
    def __init__(self, date, state):
        self.date = date
        self.state = state

class TempChange:
    def __init__(self, date, idealTemp):
        self.date = date
        self.idealTemp = idealTemp