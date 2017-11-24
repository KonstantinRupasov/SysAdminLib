"""
1cv8.exe functionality wrapper
Command line and Designer Agent functionality only
"""

class Cv8Class(object):
    """
    Each object of the class represents 1cv8.exe
    of the specific version of 1C:Enterprise
    on the local computer
    """

    def __init__(
            self,
            path
    ):
        """
        Checks if 1cv8.exe exists
        """
        # Attributes list
        self.path = path
        # Attributes initialization
        self.refresh()
        pass

    #--------------------------------------------
    # ---------------- PUBLIC -------------------
    #--------------------------------------------
    def refresh(self):
        """
        Called from __init__
        Initialises object attributes (see the complete list in self.__init__())
        Can be called explicitly to reinitialize the attributes
        """
        pass

    def dump_ib(self, infobase):
        pass
    #---------------------------------------------
    # ---------------- PRIVATE -------------------
    #---------------------------------------------
        