from guy import Guy
from backend import Backend

class Simple(Guy):
    """<button onclick="self.test()">test</button>"""
    
    def __init__(self):
        super().__init__()
        self.backend = Backend(self)
    
    async def test(self):
        print("Your name is", await self.js.prompt("What's your name ?") )

if __name__ == "__main__":
    app=Simple()
    app.run()
