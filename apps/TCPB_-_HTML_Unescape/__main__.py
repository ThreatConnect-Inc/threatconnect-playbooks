"""Set App lib directory for current version of Python"""
import os
# import signal
import subprocess
import sys

__version__ = '1.0.2'


class AppLib(object):
    """Set App Lib Directory"""
    def __init__(self):
        """Initialize App properties."""
        # NOTE: TC Core will handle sending kill to child. Then tcex has it's own logic
        #       to handle graceful shutdown.
        # signal.signal(signal.SIGINT, self.signal_handler)
        # signal.signal(signal.SIGTERM, self.signal_handler)
        self._app_process = None
        self._lib_directories = None

        # the lib directory for the current version of Python
        self.lib_directory = None

        # All Python Version that will be searched
        self.lib_major_version = 'lib_{}'.format(sys.version_info.major)
        self.lib_minor_version = '{}.{}'.format(self.lib_major_version, sys.version_info.minor)
        self.lib_micro_version = '{}.{}'.format(self.lib_minor_version, sys.version_info.micro)

    def find_lib_directory(self):
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
    def lib_directories(self):
        """Get all "lib" directories."""
        if self._lib_directories is None:
            self._lib_directories = []
            app_path = os.getcwd()
            contents = os.listdir(app_path)
            for c in contents:
                # ensure content starts with lib, is directory, and is readable
                if c.startswith('lib') and os.path.isdir(c) and (os.access(c, os.R_OK)):
                    self._lib_directories.append(c)
        return sorted(self._lib_directories, reverse=True)

    def run_app(self):
        """Run the App as a subprocess."""
        # Update system arguments
        sys.argv[0] = sys.executable
        sys.argv[1] = '{}.py'.format(sys.argv[1])

        # Make sure to exit with the return value from the subprocess call
        self._app_process = subprocess.Popen(sys.argv)
        return self._app_process.wait()  # returns exit code

    # def signal_handler(self, signal_interrupt, frame):
    #     """Handle signal interrupts."""
    #     self._app_process.send_signal(signal_interrupt)
    #     if signal_interrupt in (2, 15):  # SIGINT, SIGTERM
    #         sys.exit(1)

    @staticmethod
    def update_environment(lib_directory):
        """Run the App as a subprocess."""
        # Use this if you want to include modules from a subfolder
        # lib_path = os.path.realpath(
        #     os.path.abspath(
        #         os.path.join(
        #             os.path.split(inspect.getfile(inspect.currentframe()))[0], lib_directory)))
        lib_path = os.path.join(os.getcwd(), lib_directory)
        if 'PYTHONPATH' in os.environ:
            os.environ['PYTHONPATH'] = '{}{}{}'.format(
                lib_path, os.pathsep, os.environ['PYTHONPATH'])
        else:
            os.environ['PYTHONPATH'] = '{}'.format(lib_path)


if __name__ == '__main__':
    al = AppLib()

    # find the optimal App Lib directory
    ld = al.find_lib_directory()

    # No reason to continue if no appropriate lib directory found
    if ld is None:
        print('Failed to find lib directory ({}).'.format(al.lib_directories))
        sys.exit(1)

    # update the OS environment for lib_directory path
    al.update_environment(ld)

    # run the App
    rc = al.run_app()

    # exit with the Apps exit code
    sys.exit(rc)
