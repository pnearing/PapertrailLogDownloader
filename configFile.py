#!/usr/bin/env python3
"""
    File: config_file.py: Config file module.
        Classes:
            ConfigFileError(Exception): Errors generated by ConfigFile.
            ConfigFile(object): Manage a config file.

        Notes:
            Requires a file called common.py, with the variable SETTINGS to be defined.
            SETTINGS must also be JSON serializable.
"""
from typing import Optional
import os
import json
import stat

CAN_LOCK: bool = False
try:
    from fileLocks import LockFile, FileLockTimeoutError, FileLockError, FileUnlockError
    CAN_LOCK = True
except ModuleNotFoundError:
    pass


class ConfigFileError(Exception):
    """
        Config file exception.
            Defines:
                .error_number : int, The error_number number.
                .error_message : str, The message associated with the error_number.
                .str_args : Optional[str], The result of str(err.args) on the error that occurred.
    """
    _error_messages: dict[int, str] = {
        0: "No error_number.",
        1: "Unspecified error_number.",
        2: "Module not found, you must create a module called common.py.",
        3: "Variable not found, you must create a variable of SETTINGS in common.py",
        4: "File not found, user specified config file doesn't exist",
        5: "Permission denied while creating default config _directory.",
        6: "Permission denied while attempting to write to config file.",
        7: "Permission denied while attempting to read from config file.",
        8: "JSON Decode error_number.",
        9: "File not found, default config file doesn't exist.",
        10: "Timeout while attempting to lock file.",
        11: "Failure while attempting to unlock file.",
        12: "Failure while attempting to lock file.",
        13: "TypeError, config_name must be a str.",
        14: "TypeError, file_path must be str or None.",
        15: "TypeError, create_default must be a bool.",
        16: "TypeError, do_load must be a bool.",
        17: "TypeError, set_permissions must be int or None.",
        18: "Permission error when setting permissions of config file.",
        19: "OSError when setting permissions of config file.",
        20: "TypeError, enforce_permissions must be a bool.",
        21: "Permissions of config file are not as expected.",
        22: "ValueError, if enforce_permissions is true, set_permissions can not be None.",
    }

    def __init__(self,
                 error_number: int,
                 error_message: Optional[str] = None,
                 str_args: Optional[str] = None,
                 *args: object
                 ) -> None:
        """
        Initialize a config file error.
        :param error_number: int: The error number.
        :param error_message: Optional[str]: The error message.
        :param str_args: Optional[str]: The result of str(err.args) on the error that has occurred.
        :param args: object: Additional arguments.
        """
        super().__init__(*args)
        self.error_number = error_number
        if error_message is None:
            self.error_message = self._error_messages[error_number]
        else:
            self.error_message = error_message
        self.str_args = str_args
        return


# Make sure we have common:
try:
    import common
except ModuleNotFoundError as e:
    raise ConfigFileError(error_number=2, str_args=str(e.args))
except ImportError as e:
    raise ConfigFileError(error_number=3, str_args=str(e.args))
# Make sure we have common.SETTINGS:
try:
    from common import SETTINGS
except ModuleNotFoundError as e:
    raise ConfigFileError(error_number=2, str_args=str(e.args))
except ImportError as e:
    raise ConfigFileError(error_number=3, str_args=str(e.args))


class ConfigFile(object):
    """Class to store a config file."""

    def __init__(
            self,
            config_name: str,
            file_path: Optional[str] = None,
            create_default: bool = True,
            do_load: bool = True,
            set_permissions: Optional[int] = None,
            enforce_permissions: bool = False,
    ) -> None:
        """
        Initialize the config file.
        :param config_name: str: The configuration name, used for default _directory and file names.
        :param file_path: Optional[str]: The _path to a user specified config file.
        :param create_default: bool: Create default _directory and config file.
        :param do_load: bool: Load the config immediately
        :param set_permissions: Optional[int]: If set will set the permissions of the file to given number,
                                                If not set, will skip setting permissions all together.
        :param enforce_permissions: bool: Throw an error if permissions of a file are wrong.
        :raises ConfigFileError: On permission, file not found errors, json decode error.
        """
        # Argument checks:
        if not isinstance(config_name, str):
            raise ConfigFileError(13)
        if file_path is not None and not isinstance(file_path, str):
            raise ConfigFileError(14)
        if not isinstance(create_default, bool):
            raise ConfigFileError(15)
        if not isinstance(do_load, bool):
            raise ConfigFileError(16)
        if set_permissions is not None and not isinstance(set_permissions, int):
            raise ConfigFileError(17)
        if not isinstance(enforce_permissions, bool):
            raise ConfigFileError(20)
        # Value check arguments:
        if enforce_permissions and set_permissions is None:
            raise ConfigFileError(22)
        # Set vars:
        self._path: str
        self._file_name: str
        self._directory: str
        self._lock: Optional[LockFile] = None
        self._lock_id: str = "<configFile.py>"
        self._permissions: Optional[int] = set_permissions
        self._enforce_permissions: bool = enforce_permissions
        # User selected config file:
        if file_path is not None:
            if not os.path.exists(file_path):
                raise ConfigFileError(error_number=4)
            self._file_name = os.path.split(file_path)[-1]
            self._directory = os.path.join(*os.path.split(file_path)[0:-1])
            self._path = file_path
            # Create lock file:
            if CAN_LOCK:
                self._lock = LockFile(file_path=self._path, lock_id=self._lock_id)
        # Generated default config file:
        else:
            self._file_name = config_name + '.config'
            self._directory = os.path.join(os.environ.get("HOME"), '.config', config_name)
            self._path = os.path.join(self._directory, self._file_name)
            # Create lock file:
            if CAN_LOCK:
                self._lock = LockFile(file_path=self._path, lock_id="<configFile.py>")
            if not os.path.exists(self._directory):
                # If create_default is false, raise error_number:
                if not create_default:
                    raise ConfigFileError(error_number=9)
                # Create containing directory if it doesn't exist:
                try:
                    os.makedirs(self._directory)
                except PermissionError as err:
                    raise ConfigFileError(error_number=5, str_args=str(err.args))
                except FileNotFoundError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
                except FileExistsError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
                except OSError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
            if not os.path.exists(self.path):
                # If create_default is false, raise error_number:
                if not create_default:
                    raise ConfigFileError(error_number=9)
                # Create the config file with current settings if it doesn't exist.
                # Open file:
                try:
                    if CAN_LOCK:
                        self._lock.lock(do_raise=True, timeout=5)
                    file_handle = open(self.path, 'w')
                except PermissionError as err:
                    raise ConfigFileError(error_number=6, str_args=str(err.args))
                except FileNotFoundError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
                except OSError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
                except FileLockTimeoutError as err:
                    raise ConfigFileError(error_number=10, str_args=err.error_message)
                except FileLockError as err:
                    raise ConfigFileError(error_number=12, str_args=err.error_message)
                # Write JSON and close file:
                try:
                    file_handle.write(json.dumps(common.SETTINGS, indent=4))
                    file_handle.close()
                    if CAN_LOCK:
                        self._lock.unlock(do_raise=True)
                except OSError as err:
                    raise ConfigFileError(error_number=1, str_args=str(err.args))
                except FileUnlockError as err:
                    raise ConfigFileError(error_number=11, str_args=err.error_message)
                # Set the permissions of the file:
                if set_permissions is not None:
                    try:
                        os.chmod(self.path, set_permissions)
                    except PermissionError as err:
                        raise ConfigFileError(error_number=18, str_args=str(err.args))
                    except OSError as err:
                        raise ConfigFileError(error_number=19, str_args=str(err.args))
        # Load the config file
        if do_load:
            self.load()
        return

    @property
    def path(self) -> str:
        """
        Returns the full _path of the config file.
        :return: str
        """
        return self._path

    @property
    def file_name(self) -> str:
        """
        Returns the file name of the config file.
        :return: str
        """
        return self._file_name

    @property
    def directory(self) -> str:
        """
        Returns the directory containing the config file.
        :return: str
        """
        return self._directory

    def load(self) -> None:
        """
        Load the config file:
        :return: None
        :raises ConfigFileError on file
        """
        global CAN_LOCK
        # Check permissions:
        if self._enforce_permissions:
            st = os.stat(self.path)
            if oct(st.st_mode)[-3:] != oct(self._permissions)[-3:]:
                raise ConfigFileError(21)
        # Open the file for reading:
        try:
            # Lock the file if we can:
            if CAN_LOCK:
                self._lock.lock(lock_type='READ', do_raise=True, timeout=5)
            file_handle = open(self.path, 'r')
        except FileNotFoundError as err:
            raise ConfigFileError(error_number=4, str_args=str(err.args))
        except PermissionError as err:
            raise ConfigFileError(error_number=7, str_args=str(err.args))
        except OSError as err:
            raise ConfigFileError(error_number=1, str_args=str(err.args))
        except FileLockTimeoutError as err:
            raise ConfigFileError(error_number=10, str_args=str(err.args))
        except FileLockError as err:
            raise ConfigFileError(error_number=12, str_args=err.error_message)

        # Load the JSON and close the file:
        try:
            common.SETTINGS = json.loads(file_handle.read())
            file_handle.close()
            # Unlock the file if it was locked.
            if CAN_LOCK:
                self._lock.unlock(do_raise=True)
        except json.JSONDecodeError as err:
            raise ConfigFileError(error_number=8, str_args=err.msg)
        except IOError as err:
            raise ConfigFileError(error_number=1, str_args=str(err.args))
        except FileUnlockError as err:
            raise ConfigFileError(error_number=11, str_args=err.error_message)
        return

    def save(self) -> None:
        """Save the configuration."""
        # Open the file for writing:
        try:
            # Lock the file if we can:
            if CAN_LOCK:
                self._lock.lock(do_raise=True, timeout=5)
            file_handle = open(self.path, 'w')
        except PermissionError as err:
            raise ConfigFileError(error_number=6, str_args=str(err.args))
        except OSError as err:
            raise ConfigFileError(error_number=1, str_args=str(err.args))
        except FileLockTimeoutError as err:
            raise ConfigFileError(error_number=10, str_args=err.error_message)
        except FileLockError as err:
            raise ConfigFileError(error_number=12, str_args=err.error_message)
        # Write the JSON, and close the file:
        try:
            file_handle.write(json.dumps(common.SETTINGS, indent=4))
            file_handle.close()
            # Unlock the file if it was locked:
            if CAN_LOCK:
                self._lock.unlock(do_raise=True)
        except IOError as err:
            raise ConfigFileError(error_number=1, str_args=str(err.args))
        except FileUnlockError as err:
            raise ConfigFileError(error_number=11, str_args=err.error_message)
        return
