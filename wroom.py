import wx

class Example(wx.Frame):
           
    def __init__(self, *args, **kw):
        super(Example, self).__init__(*args, **kw) 
        connections = [{"name":"ale", "playerID": 1, "addr":12345, "game":"somegame"},
                    {"name":"mar", "playerID": 2, "addr":54321, "game":"somegame"}]

        self.InitUI(connections)
        
    def InitUI(self, connections):

        pnl = wx.Panel(self)

        font = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD)
        heading = wx.StaticText(self, label='Testing wxpython', pos=(130, 15))
        heading.SetFont(font)

        wx.StaticLine(self, pos=(25, 50), size=(300,1))

        wx.StaticText(self, label=connections[0].get("name"), pos=(25, 80))
        wx.StaticText(self, label=connections[1].get("name"), pos=(25, 100))

        wx.StaticText(self, label=str(connections[0].get("addr")), pos=(100, 80))
        wx.StaticText(self, label=str(connections[1].get("addr")), pos=(100, 100))

        wx.StaticText(self, label=str(connections[0].get("game")), pos=(250, 80))
        wx.StaticText(self, label=str(connections[1].get("game")), pos=(250, 100))

        wx.StaticLine(self, pos=(25, 260), size=(300,1))

        tsum = wx.StaticText(self, label='164 336 000', pos=(240, 280))
        sum_font = tsum.GetFont()
        sum_font.SetWeight(wx.BOLD)
        tsum.SetFont(sum_font)

        btn = wx.Button(self, label='Close', pos=(140, 310))

        btn.Bind(wx.EVT_BUTTON, self.OnClose)        
        
        self.SetSize((360, 380))
        self.SetTitle('wx.StaticLine')
        self.Centre()
        self.Show(True)      
        
    def OnClose(self, e):
        
        self.Close(True)    
                      
def main():
    
    ex = wx.App()
    Example(None)
    ex.MainLoop()    

if __name__ == '__main__':
    main()
