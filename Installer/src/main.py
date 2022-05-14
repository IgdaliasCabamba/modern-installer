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
    
    async def get_backend(self):
        return self.backend
    
    async def install(self, data):
        self.backend.install(data)
    
    async def cancel(self):
        self.backend.exit()

if __name__ == "__main__":
    app=Installer()
    app.run()
