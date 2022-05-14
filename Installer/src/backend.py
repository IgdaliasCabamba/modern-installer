import pathlib
import os
import sys
import hjson
import tarfile
import shutil
import getpass
import desktop_file

if getattr(sys, "frozen", False):
    root_path = os.path.dirname(os.path.realpath(sys.executable))
else:
    root_path = os.path.dirname(os.path.realpath(__file__))

DEFAULT_APPS_SRC_FOLDER = os.path.join(str(pathlib.Path.home()), f"{getpass.getuser()}-NIC-Apps", "Sources")
DEFAULT_APPS_IMAGE_FOLDER = os.path.join(str(pathlib.Path.home()), f"{getpass.getuser()}-NIC-Apps", "Images")
DATABASE_PATH = os.path.join(str(pathlib.Path.home()), f"{getpass.getuser()}-NIC-Apps_", ".data", "storage"),
DESKTOP_FILES_PATH = os.path.join(str(pathlib.Path.home()), f"{getpass.getuser()}-NIC-Apps_", ".data", "desktop-files")

with open(os.path.join(root_path, "config.json"), "r") as fp:
    SETTINGS = hjson.load(fp)

require_dirs = [
        DEFAULT_APPS_SRC_FOLDER, DEFAULT_APPS_IMAGE_FOLDER,
        DATABASE_PATH, DESKTOP_FILES_PATH 
    ]

for require_dir in require_dirs:
    if not os.path.exists(require_dir):
        os.makedirs(require_dir)

def get_desktop_file(data, exec_path):
    desktop_path = desktop_file.getDesktopPath()
    shortcut = desktop_file.Shortcut(desktop_path, data["id"], exec_path)
    return shortcut

def get_menu_shortcut(data, exec_path):
    menu_path = desktop_file.getMenuPath()
    shortcut = desktop_file.Shortcut(menu_path, data["id"], exec_path)
    return shortcut
    
class Backend:
    def __init__(self, frontend):
        self._ui = frontend
        
        try:
            if SETTINGS["bin-type"] in {"source", 0}: 
                self.type_of_bin = 0
                self.bin = os.path.join(root_path, "bin", "package.tar.xz")

            elif SETTINGS["bin-type"] in {"image", 1}:
                self.type_of_bin = 1
                self.bin = os.path.join(root_path, "bin", "package.AppImage")
        
            else:
                self.exit()
        except Exception as e:
            print(e)
            self.exit()
        
        if SETTINGS["setup-file"] is None:
            self.setup_file = None
        else:
            self.setup_file = os.path.join(root_path, "install", SETTINGS["setup-file"])

    def install(self, data):
        if data["folder"] is not None:
            install_folder = os.path.join(str(pathlib.Path.home()), os.data["folder"])
        else:
            if self.type_of_bin == 0:
                install_folder = os.path.join(DEFAULT_APPS_SRC_FOLDER, data["name"])
                unpack = tarfile.open(self.bin)
                unpack.extractall(install_folder)
                unpack.close()
            
            else:
                install_folder = os.path.join(DEFAULT_APPS_IMAGE_FOLDER, data["name"])
                shutil.copyfile(self.bin, install_folder)
        
        if self.setup_file is not None:
            setup = os.path.join(install_folder, "setup")
            shutil.copyfile(self.setup_file, setup)

            os.system(f"chmod 774 {setup}")
            os.system(f'.{setup}')
        
            #os.system(f'echo "{sudo_pw}" | sudo -S chmod 774 {setup}')
            #os.system(f'echo "{sudo_pw}" | sudo -S {setup}')
        
            #os.remove(setup)
            shutil.rmtree(setup)
        
        if isinstance(SETTINGS["desktop-file"], dict):
            data = SETTINGS["desktop-file"]
            desktop_file = get_desktop_file(data, self.install_folder)

        if data["disconnect"]:
            self.exit()
    
    def exit(self):
        os._exit(0)