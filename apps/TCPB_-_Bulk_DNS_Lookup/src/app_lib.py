"""Class to set App lib directory for current version of Python"""
# standard library
import os
import sys


class AppLib:
    """Set App Lib Directory"""

    def __init__(self):
        """Initialize App properties."""
        self._lib_directories = None

        # All Python Version that will be searched
        self.lib_major_version = f'lib_{sys.version_info.major}'
        self.lib_minor_version = f'{self.lib_major_version}.{sys.version_info.minor}'
        self.lib_micro_version = f'{self.lib_minor_version}.{sys.version_info.micro}'

    def find_lib_directory(self) -> str:
        """Find the optimal lib directory."""
        lib_directory = None
        if self.lib_micro_version in self.lib_directories:
            lib_directory = self.lib_micro_version
        elif self.lib_minor_version in self.lib_directories:
            lib_directory = self.lib_minor_version
        elif self.lib_major_version in self.lib_directories:
            lib_directory = self.lib_major_version
        else:
            for lv in [self.lib_micro_version, self.lib_minor_version, self.lib_major_version]:
                for d in self.lib_directories:
                    if lv in d:
                        lib_directory = d
                        break
                else:
                    continue
                break
        return lib_directory

    @property
    def lib_directories(self) -> list:
        """Return all "lib_" directories."""
        if self._lib_directories is None:
            self._lib_directories = []
            app_path = os.getcwd()
            contents = os.listdir(app_path)
            for c in contents:
                # ensure content starts with lib, is directory, and is readable
                if c.startswith('lib') and os.path.isdir(c) and (os.access(c, os.R_OK)):
                    self._lib_directories.append(c)
        return sorted(self._lib_directories, reverse=True)

    def update_path(self) -> None:
        """Update sys path to ensure all required modules can be found.

        All Apps must be able to access included modules, this method will ensure that the system
        path has been updated to include the "cwd" and the proper "lib_" directories.
        """
        lib_directory = self.find_lib_directory()
        lib_latest = os.path.join(os.getcwd(), 'lib_latest')

        # insert the appropriate lib_directory into system path if found, otherwise insert
        # lib_latest directory into the system Path. This entry will be bumped to index 1
        # after adding the current working directory.
        if lib_directory is None:
            lib_directory = lib_latest
        sys.path.insert(0, os.path.join(os.getcwd(), lib_directory))

        # insert the current working directory into the system Path for the App, ensuring that it is
        # always the first entry in the list.
        cwd = os.getcwd()
        try:
            sys.path.remove(cwd)
        except ValueError:
            pass
        sys.path.insert(0, cwd)
