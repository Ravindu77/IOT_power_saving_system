import json

class Reading:
    def __init__(self, date, temp, humid):
        self.date = date
        self.temp = temp
        self.humid = humid
    
    @classmethod
    def from_json(cls, jsonStr):
        jsonStr = json.loads(jsonStr)
        return cls(**jsonStr)

class Power:
    def __init__(self, date, state):
        self.date = date
        self.state = state
    
    @classmethod
    def from_json(cls, jsonStr):
        jsonStr = json.loads(jsonStr)
        return cls(**jsonStr)

class TempChange:
    def __init__(self, date, idealTemp):
        self.date = date
        self.idealTemp = idealTemp
    
    @classmethod
    def from_json(cls, jsonStr):
        jsonStr = json.loads(jsonStr)
        return cls(**jsonStr)