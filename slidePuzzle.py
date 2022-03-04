import wx
from board import Board

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):
        wx.Frame.__init__(self, parent, title=title, size=size)
        mainPanel = wx.Panel(self)

        self.board = Board(self, (400,400), (20,50))
    
    def update_game_state(self):
        if self.board.ordered():
            wx.MessageDialog(self, "You've won!!!", caption="Victory").ShowModal()
            self.board.stop_game()
        
    def OnExit(self, event):        
        self.Close(True)    

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title='Slide Puzzle', size=(500,500))
    frame.Show()
    app.MainLoop()