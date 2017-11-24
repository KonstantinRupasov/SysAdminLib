"""
Stable API, providing higher-level tools with all locally available administrative functions

Works as a proxy object for:
    - RAS/RAC
    - 1cv8.exe in command-line mode and designer agent mode
    - Event Log

Uses low-level  classes from ./lib modules
"""

import time
import os
import platform
import logging
import src.lib.rac as rac
import src.lib.cv8 as cv8
import src.lib.elog as elog

class ThePlatformClass(object):
    """
    Each objects of the class represents a single 1C:Enterprise platform installation on the local computer
    """

    def __init__(
            self,
            path=None,                   # 1C:Enterprise installation root catalog. 1C default catalog by default
            version=None,                # 1C:Enterprise version. Last version installed by default
            bit_version='32',            # 1C:Enterprise bit version ('32' or '64')
            cluster='localhost',         # 1C:Enterprise cluster name
            log_level=logging.WARN,      # Default logging level
            log_path=None,               # Path to logging directory
            log_to_con=False             # Log to console (as well as to the log file)
    ):
        """
        Class constructor
        Parameters:
            - path: 1C:Enterprise installation root catalog. Default depends on the OS type
            - version: 1C:Enterprise version. Default: the latest locally installed version
        """
        # Check params
        if bit_version not in ('32', '64'):
            raise ValueError('bit_version parameter must be in (''32'', ''64'', None)')
        # Init logging
        self.logger = self._init_logger(log_level, log_path, log_to_con)
        # Attributes list
        self.os_type = None                 # Windows, Linux, macOS
        self.os_version = None              # OS version description
        self.os_architecture = None         # 32bit or 64bit
        self.bin_path = None                # Full path to executives
        self.rac = None                     # RacClass Object. Used to perform RAC actions
        self.cv8 = None                     # 1cv8Class object
        self.infobases = None               # Infobases list
        self.event_log = None               # EventLog object
        # Attributes initialization
        self.refresh(path, version, bit_version)

    def _init_logger(self, log_level, log_path, log_to_con):
        """
        Initialize logging
        """
        logger = logging.getLogger('root')
        logger.setLevel(log_level)
        # Init the logging directory
        if log_path is None:
            log_path = os.path.curdir + os.path.sep + 'LOGS'
        if not os.path.exists(log_path):
            os.makedirs(log_path)
        # Init handlers and formatter
        formatter = logging.Formatter('%(asctime)-15s %(name)-10s %(levelname)-5s %(message)s')
        log_file_name = time.strftime('%Y%m%d_%H%M%S.log')
        file_handler = logging.FileHandler(log_path + os.path.sep + log_file_name, 'w')
        file_handler.formatter = formatter
        logger.addHandler(file_handler)
        if log_to_con:
            con_handler = logging.StreamHandler()
            logger.addHandler(con_handler)
        # Log init info
        logger.info('Logger is initialised successfully')
        logger.debug('LOG filename: %s', log_file_name)
        return logger

    #--------------------------------------------
    # ---------------- PUBLIC -------------------
    #--------------------------------------------
    def refresh(self, path, version, bit_version):
        """
        Called from __init__
        Initialises object attributes (see the complete list in self.__init__())
        Can be called explicitly to reinitialize the attributes
        """
        self.os_type, self.os_version, self.os_architecture = self._get_os_info()
        self.bin_path = self._get_bin_path(path, version, bit_version)
        self.rac = rac.RacClass(self.bin_path)
        self.cv8 = cv8.Cv8Class(self.bin_path)
        self.infobases = self.rac.get_infobases()
        self.event_log = elog.EventLog()

    def update_ibs_cf(
            self,
            infobases,              # List of infobases to update: [{ibname:<ibname>, login:<login>, password:<password>}]
            cf_file                 # CF file to take the new configuration from
        ):
        """
        Updates the infobases' configuration to the new version from CF file
        Parameters:
            - infobases: [{ibname:<ibname>, login:<login>, password:<password>}]
        """
        for infobase in infobases:
            self.update_ib_cf(infobase, cf_file)
    
    def update_ib_cf(
            self,
            infobase,               # {ibname:<ibname>, login:<login>, password:<password>}
            cf_file                 # CF file to take the new configuration from
        ):
        """
        Update a single infobase configuration to the new version from CF file
        """
        self.rac.sessions_lock(infobase, 'on')                      # Locking new sessions
        self.rac.disconnect_users(infobase)                         # Disconnecting users
        dt_file = self.dump_ib_dt(infobase)                         # Saving DT
        try:
            pass
            #self.cv8.update_cf(infobase, cf_file)          # Update CF 
        except Exception as exc:
            self.restore_ib_dt(infobase, dt_file)                   # Restore the initial state (last DT)
            self.rac.sessions_lock(infobase, 'off')                 # Unlock new sessions
            raise exc

    def dump_ib_dt(
            self,
            infobase,              # {ibname:<ibname>, login:<login>, password:<password>}
            dt_file=''             # Name of DT file. Default: temp file (the name will be returned)
        ):
        """
        Dumps the infobase to DT file
        Returns the filename
        """
        pass
        #self.cv8.dump_ib(infobase)

    def restore_ib_dt(
            self,
            infobase,               # {ibname:<ibname>, login:<login>, password:<password>}
            dt_file                 # Name of DT file. Default: temp file (the name will be returned)
        ):
        """
        Restores the infobase from DT file
        """
        pass

    #---------------------------------------------
    # ---------------- PRIVATE -------------------
    #---------------------------------------------
    def _get_os_info(self):
        """
        Get the local computer OS type and the OS version
        """
        _system = platform.system()
        _platform = platform.platform()
        _architecture = platform.architecture()[0]
        self.logger.info('OS type: %s', _system)
        self.logger.info('OS version: %s', _platform)
        self.logger.info('OS architecture: %s', _architecture)
        return _system, _platform, _architecture

    def _get_bin_path(self, path, version, bit_version):
        """
        Get the full path to 1C:Enterprise bin catalog
        depending on the OS type
        """
        if path is None:
            if self.os_type == 'Darwin':
                bin_path = '/Applications/1cv8-{version}.app/Contents/MacOS'
                pass
            elif self.os_type == 'Linux':
                bin_path = '/opt/1C/v{minor_version}/x86_{bit_version}}'
            elif self.os_type == 'Windows':
                bin_path = 'C:\\Program Files{x86}\\1cv8\\{version}\\bin'
            else:
                pass

#---------------------------------------------
# ---------------- TESTING -------------------
#---------------------------------------------
if __name__ == '__main__':
    PLATFORM = ThePlatformClass(log_level=logging.DEBUG, log_to_con=True)
    PLATFORM.logger.info('ThePlatformClass is initialised successfully')
