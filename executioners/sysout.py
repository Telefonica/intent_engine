from queue import Queue

class sysout():

    def __init__(self,queue : Queue):
        self.__name="sysout"
        self.__args=[]
        self.__queue=queue
    def execute(self,string):
        print(" -> -> Executing: ", string, " <- <-")
        # True if no error
        return True