import wx
from board import Board

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title=title, size=size)
        mainPanel = wx.Panel(self)
        self.moveCounter = 0        
        self.gameTime = 0
        self.board = Board(self, (400,400), (20,100))

        font = wx.Font((0,25), wx.FONTFAMILY_SWISS, wx.NORMAL, wx.FONTWEIGHT_BOLD)

        self.moveLabel = wx.StaticText(self, label="Moves: 0", pos=(20,60), size=(150,25), style=0)        
        self.moveLabel.SetFont(font)

        self.timeLabel = wx.StaticText(self, label="Time: 00:00", pos=(270,60), size=(150,25), style=wx.ALIGN_RIGHT)        
        self.timeLabel.SetFont(font)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_time, self.timer)

        restartButton = wx.Button(self, label="Restart game", pos=(320,10), size=(100,35), style=0)
        restartButton.Bind(wx.EVT_BUTTON, self.start_game)

        self.start_game()
    
    def start_game(self, e=None):        
        self.moveCounter = 0        
        self.gameTime = 0
        self.board.start_game()
        self.timer.Start(1000)        
        
        self.moveLabel.SetLabel("Moves: 0")
        self.timeLabel.SetLabel("Time: 00:00")
        

    def update_game_state(self):
        self.moveCounter += 1
        self.moveLabel.SetLabel("Moves: {}".format(self.moveCounter))
        
        if self.board.ordered():
            self.timer.Stop()
            self.board.stop_game()
            wx.MessageDialog(self, "You've won!!!", caption="Victory").ShowModal()
    
    def update_time(self, e):
        self.gameTime += 1

        hrs = self.gameTime // 3600
        mins = (self.gameTime - hrs*3600) // 60
        secs = self.gameTime - hrs*3600 - mins*60        
        self.timeLabel.SetLabel("Time: {:0>2}:{:0>2}".format(mins,secs))

        
        
    def OnExit(self, event):        
        self.Close(True)    

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title='Slide Puzzle', size=(500,550))
    frame.Show()
    app.MainLoop()