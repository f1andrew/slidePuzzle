import wx
import random

class MainFrame(wx.Frame):
    def __init__(self, parent, title, size):        
        wx.Frame.__init__(self, parent, title=title, size=size)
        
        self.puzzle_width = self.GetSize()[0]
        self.puzzle_height = self.GetSize()[1]
        self.cols = 3
        self.rows = 3
        self.tile_width = self.puzzle_width // self.cols
        self.tile_height = self.puzzle_height // self.rows
        self.tiles = []
        self.tile_indexes = []
        self.removed_tile = None
        self.victory_state = False

        #panel = wx.Panel(self)
        self.source_image = wx.Image("nasa_logo.jpg", type=wx.BITMAP_TYPE_ANY, index=-1)        
        self.source_image.Rescale(self.puzzle_width, self.puzzle_height, wx.IMAGE_QUALITY_HIGH)
        self.splitImage(self.source_image)
        self.shuffleTiles(50)


        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_UP, self.mousePress)
    
    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.SetPen(wx.Pen('#000000', 3, wx.PENSTYLE_SOLID))
        dc.SetBrush(wx.Brush('#4c4c4c', wx.BRUSHSTYLE_TRANSPARENT))

        for y in range(self.rows):
            for x in range(self.cols):
                x_offset = x*self.tile_width
                y_offset = y*self.tile_height
                if self.tile_indexes[y][x] != None:
                    tile_index = self.tile_indexes[y][x]
                    dc.DrawBitmap(wx.Bitmap(self.tiles[tile_index], wx.BITMAP_TYPE_ANY), x=x_offset, y=y_offset)
                if not self.victory_state:
                    dc.DrawRectangle(x_offset, y_offset, self.tile_width, self.tile_height)

    def mousePress(self, event): 
        if not self.victory_state:       
            pressed_tile_x = event.GetX() // self.tile_width
            pressed_tile_y = event.GetY() // self.tile_height
            if pressed_tile_x < self.cols and pressed_tile_y < self.rows:        
                self.moveTile(pressed_tile_x, pressed_tile_y)
                self.Refresh()
        event.Skip()

    def victory_routine(self):
        wx.MessageDialog(self, "You've won!!!", caption="Victory").ShowModal()
        self.tile_indexes[self.rows-1][self.cols-1] = self.rows*self.cols-1
        self.victory_state = True

    def splitImage(self, original_image):
        self.tiles = []
        tile_counter = 0
        for y in range(self.rows):            
            row_tmp = []
            for x in range(self.cols):
                x_offset = x*self.tile_width
                y_offset = y*self.tile_height                
                img_tmp = original_image.Copy()
                img_tmp.Resize((self.tile_width, self.tile_height), (-x_offset, -y_offset))
                self.tiles.append(img_tmp)
                row_tmp.append(tile_counter)
                tile_counter += 1
            self.tile_indexes.append(row_tmp)
            

        self.blank_tile_x = self.rows-1
        self.blank_tile_y = self.cols-1        
        self.tile_indexes[self.blank_tile_y][self.blank_tile_x] = None
 
    def moveTile(self, x, y, is_shuffle=False):
        distance_to_blank_y = self.blank_tile_y - y
        distance_to_blank_x = self.blank_tile_x - x
        distance_to_blank = abs(distance_to_blank_y ) + abs(distance_to_blank_x)
        if(distance_to_blank == 1):
            self.tile_indexes[self.blank_tile_y][self.blank_tile_x] = self.tile_indexes[y][x]
            self.tile_indexes[y][x] = None
            self.blank_tile_y = y
            self.blank_tile_x = x

            if not is_shuffle and self.check_is_won():                
                self.victory_routine()

    def shuffleTiles(self, n_moves):
        for i in range(n_moves):
            rand_x = random.randrange(self.cols)
            rand_y = random.randrange(self.cols)
            self.moveTile(rand_x, rand_y, True)

    def check_is_won(self):
        tile_counter = 0
        for y in range(self.rows):
            for x in range(self.cols):
                if self.tile_indexes[y][x] != tile_counter and tile_counter != self.rows*self.cols-1:
                    return False
                tile_counter +=1
        return True

    def OnExit(self, event):        
        self.Close(True)    

if __name__ == '__main__':
    app = wx.App()
    frame = MainFrame(None, title='Slide Puzzle', size=(400,400))
    frame.Show()
    app.MainLoop()