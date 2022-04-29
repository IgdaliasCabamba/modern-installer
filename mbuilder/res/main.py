import sys
sys.dont_write_bytecode = True

import guy
from guy import Guy
from backend import *

guy.FOLDERSTATIC = os.path.join(root_path, "ui")

class Installer(Guy):
    
    def __init__(self):
        super().__init__()
        self.backend = Backend(self)
    
    def render(self, path):
        with open(os.path.join(root_path, guy.FOLDERSTATIC, "index.html")) as fid:
            buf=fid.read()
        
        return buf
    
    async def install(self, data):
        sudo_pw = None
        if data["require"]["sudo"]:
            sudo_pw = await self.js.prompt("Please enter sudo password")
        self.backend.install(data, sudo_pw)
    
    async def cancel(self):
        self.backend.exit()

if __name__ == "__main__":
    app=Installer()
    app.run()
