import wx

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):        
        wx.Frame.__init__(self, parent, title=title, size=size)
        
        self.puzzle_width = self.GetSize()[0]
        self.puzzle_height = self.GetSize()[1]
        self.cols = 3
        self.rows = 2
        self.tile_width = self.puzzle_width // self.cols
        self.tile_height = self.puzzle_height // self.rows
        self.tiles = []
        print("Tile width: ", self.tile_width)
        print("Tile height: ", self.tile_height)

        #panel = wx.Panel(self)
        self.source_image = wx.Image("nasa_logo.jpg", type=wx.BITMAP_TYPE_ANY, index=-1)        
        self.source_image.Rescale(self.puzzle_width, self.puzzle_height, wx.IMAGE_QUALITY_HIGH)
        self.splitImage(self.source_image)
        #wx.StaticBitmap(self, -1, wx.Bitmap(self.source_image, wx.BITMAP_TYPE_ANY), pos=(0, 0))

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.mousePress)
                
        #self.CreateStatusBar()
        #self.SetStatusText("Welcome to wxPython!")

    def splitImage(self, original_image):
        for y in range(self.rows):
            for x in range(self.cols):
                x_offset = x*self.tile_width
                y_offset = y*self.tile_height
                img_tmp = original_image.Copy()
                img_tmp.Resize((self.tile_width, self.tile_height), (-x_offset, -y_offset))
                self.tiles.append(img_tmp)

    
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush('#4c4c4c', wx.BRUSHSTYLE_TRANSPARENT))

        for y in range(self.rows):
            for x in range(self.cols):
                tile_index = x + y*self.cols
                x_offset = x*self.tile_width
                y_offset = y*self.tile_height
                dc.DrawBitmap(wx.Bitmap(self.tiles[tile_index], wx.BITMAP_TYPE_ANY), x=x_offset, y=y_offset)        
                dc.DrawRectangle(x_offset, y_offset, self.tile_width, self.tile_height)

    def mousePress(self, event):
        print("click")
        print("X: ", event.GetX(), "; Y: ", event.GetY())
        event.Skip()

    def OnExit(self, event):        
        self.Close(True)    

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title='Slide Puzzle', size=(400,400))
    frame.Show()
    app.MainLoop()