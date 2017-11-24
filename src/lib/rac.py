"""
RAS/RAC 1C:Enterprise utilities functionality wrapper
"""

import logging

class RacClass(object):
    """
    Each object of the class represents rac.exe utility 
    of the specific version of 1C:Enterprise
    on the local computer
    """

    def __init__(
            self,
            path
        ):
        """
        Checks if RAS is running. Run it if necessary
        Checks if RAC.exe exists
        Reads the cluster info
        """
        # Attributes list
        self.logger = logging.getLogger('root.rac')
        self.path = path
        self.cluster_info = None
        # Attributes initialization
        self.refresh()
        self.logger.info('RAS/RAC object is intialised successfully')

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
    
    def get_infobases(self):
        """
        Returns the list of infobases
        """
        pass

    def sessions_lock(self, infobase, mode):
        """
        Lock new sessions and scheduled jobs for the infobase
        Mode: ('on', 'off')
        """
        pass

    def disconnect_users(self, infobase):
        """
        Disconnect all users from the infobase
        """
        pass


    #---------------------------------------------
    # ---------------- PRIVATE -------------------
    #---------------------------------------------
