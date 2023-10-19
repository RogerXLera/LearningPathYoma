
class Skill:
    """
    This class stores the information about skills and its level.
    """

    def __init__(self,name,level,presence=0.5,probability=0.5,cluster=None,family=None):
        self.name = name
        self.level = level
        self.presence = presence
        self.probability = probability
        self.cluster = cluster
        self.family = family


    def __str__(self):
        string_ = f"{self.name}"
        return string_
    
    def __repr__(self):
        return self.name


class Job:
    """
    This class stores the information about Jobs and its methods.
    """

    def __init__(self,id,name,descriptor=None):
        self.id = id
        self.name = name
        self.descriptor = descriptor
        self.skills = [] #skills needed for obtaining the job

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.id

