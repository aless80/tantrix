import wx
import clientListener as cll
import config as cfg

class waitingRoom(wx.Frame, cll.ClientListener):
    #http://zetcode.com/wxpython/advanced/
    def __init__(self, *args, **kw):
        super(waitingRoom, self).__init__(*args, **kw)  # same as:   waitingRoom.__init__(self)
        self.InitUI()

    def startWaitingRoomUI(self):
        ex = wx.App()
        waitingRoom(None)
        ex.MainLoop()

    def InitUI(self):
        connections = [{"name":"ale", "playerID": 1, "addr":12345, "game":"somegame"},
                    {"name":"mar", "playerID": 2, "addr":54321, "game":"somegame"}]
        pnl = wx.Panel(self)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        heading = wx.StaticText(self, label='Testing wxpython', pos=(130, 15))
        heading.SetFont(font)

        wx.StaticLine(self, pos=(25, 50), size=(300,1))
        self.conn=[]
        posy = 80
        for i, c in enumerate(connections):
            self.conn.append(None)
            self.conn[i] = wx.StaticText(self, label=str(c.get("name")), pos=(25, posy))
            wx.StaticText(self, label=str(c.get("addr")), pos=(100, posy))
            wx.StaticText(self, label=str(c.get("game")), pos=(250, posy))
            self.conn[i].Bind(wx.EVT_BUTTON, self.toggleBold)
            posy += 20

        btn_wroom_exit = wx.Button(self, label='Quit', pos=(25, 310))
        btn_wroom_exit.Bind(wx.EVT_BUTTON, self.quitWaitingRoom)
        btn_wroom_ready = wx.Button(self, label='Ready', pos=(125, 310))
        btn_wroom_ready.Bind(wx.EVT_BUTTON, self.toggleReadyForGame)
        btn_wroom_solitaire = wx.Button(self, label='Solitaire', pos=(225, 310))
        btn_wroom_solitaire.Bind(wx.EVT_BUTTON, self.solitaire)

        """test bold"""
        btnBold = wx.Button(self, label='Bold', pos=(325, 310))
        btnBold.Bind(wx.EVT_BUTTON, self.toggleBold)

        self.SetSize((460, 380))
        self.SetTitle('wx.StaticLine')
        self.Centre()
        self.Show(True)

    def toggleBold(self, e):
        print(e)
        self.conn[1] = self.conn[1]
        font = self.conn[1].GetFont()
        bkg = self.conn[1].GetBackgroundColour()
        fgr = self.conn[1].GetForegroundColour()
        print(bkg)
        print(fgr)
        if bkg == (0,0,255):
            font.SetWeight(wx.NORMAL)
            self.conn[1].SetBackgroundColour((214,214,214)) # set text back color
            self.conn[1].SetForegroundColour((33,33,33)) # set text color
        elif bkg == (214,214,214):
            self.conn[1].SetBackgroundColour((0,0,255)) # set text back color
            self.conn[1].SetForegroundColour((255,0,0)) # set text color
            font.SetWeight(wx.BOLD)
        self.conn[1].SetFont(font)

    def toggleReadyForGame(self, e):
        print("toggleReadyForGame")
        self.send_to_server("toggleReady", sender = cfg.connectionID, orig = "callbacks.Callbacks.toggleReadyForGame")
        cfg.connection.Pump()

    def quitWaitingRoom(self, e):
        print("quitWaitingRoom()")
        self.send_to_server("quit", orig = "callbacks.Callbacks.quitWaitingRoom")
        self.wroom = False
        self.quit = True
        cfg.connection.Pump()

    def solitaire(self, e):
        print("solitaire")
        cfg.solitaire = True
        self.wroom = False
        #todo implement on server solitaire
        self.send_to_server("solitaire", orig = "callbacks.Callbacks.solitaire")
        cfg.connection.Pump()


                      
def main():
    ex = wx.App()
    waitingRoom(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()
