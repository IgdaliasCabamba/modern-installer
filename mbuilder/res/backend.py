import pathlib
import platformdirs
import os
import sys
import hjson
import tarfile
import shutil
import subprocess

if getattr(sys, "frozen", False):
    root_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    root_path = os.path.dirname(os.path.realpath(__file__))

class Backend:
    def __init__(self, frontend):
        self._ui = frontend
        self.bin = os.path.join(root_path, "bin", "package.tar.xz")
        self.setup_file = os.path.join(root_path, "install", "setup")

    def install(self, data, sudo_pw):
        if data["folder"] is not None:
            install_folder = data["folder"]
        else:
            install_folder = root_path
        
        setup = os.path.join(install_folder, "setup")
        
        unpack = tarfile.open(self.bin)
        unpack.extractall(install_folder)
        unpack.close()
        
        shutil.copyfile(self.setup_file, setup)
        
        if sudo_pw is None:
            os.system(f"chmod 774 {setup}")
            os.system(f'.{setup}')
        else:
            os.system(f'echo "{sudo_pw}" | sudo -S chmod 774 {setup}')
            os.system(f'echo "{sudo_pw}" | sudo -S {setup}')
        
        os.remove(setup)
        if data["disconnect"]:
            self.exit()
    
    def exit(self):
        os._exit(0)