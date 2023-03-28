from abc import abstractmethod

def abstractproperty(f):
    return property(abstractmethod(f))