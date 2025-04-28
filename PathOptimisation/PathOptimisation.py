import tkinter as tk

from PIL import Image,ImageTk 

def color_from_rgb(rgb):
    print(rgb)
    rgb = (int(rgb[0]), int(rgb[1]), int(rgb[2]))#
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   

im = Image.open('ColorTheme.bmp') # Can be many different formats.
pix = im.load()

NODE_INNER_COLOR = color_from_rgb(pix[633,233])
CANVAS_BG = color_from_rgb(pix[644,718])
SIDEBAR_BG = color_from_rgb(pix[1100, 250])

CONNECTOR_COLOR = color_from_rgb(pix[375, 260])
CONNECTOR_EASY_COLOR = color_from_rgb(pix[524, 298])
CONNECTOR_HARD_COLOR = color_from_rgb(pix[683, 385])

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600

SIDEBAR_WIDTH = 200
SIDEBAR_HEIGHT = CANVAS_HEIGHT

class PathOptimisationCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
class PathOptimisationFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.MapCanvas = PathOptimisationCanvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BG)
        self.MapCanvas.pack(side="left")
        self.MapCanvas.bind("<Button-1>", self.on_click)
        self.MapCanvas.bind("<B1-Motion>", self.on_drag)
        self.MapCanvas.bind("<ButtonRelease-1>", self.on_release)

        self.isSettingsPanelVisible = False
        self.ControlsCanvas = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)
        btn_settings = self.ControlsCanvas.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")
        self.ControlsCanvas.tag_bind(btn_settings, "<Button-1>",self.swapToSettings)
        self.ControlsCanvas.pack(side="right")  

        self.SettingsCanvas = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)
        btn_Settings = self.SettingsCanvas.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")
        self.SettingsCanvas.tag_bind(btn_settings, "<Button-1>",self.swapToSettings)
        self.SettingsCanvas.create_text(SIDEBAR_WIDTH/2, 50, text="Settings")

        self.start_x = None
        self.start_y = None
        self.current_shape = None

    def swapToSettings(self, event):
        if(self.isSettingsPanelVisible):
            self.SettingsCanvas.pack_forget()
            self.ControlsCanvas.pack(side="right")
        else:
            self.ControlsCanvas.pack_forget()
            self.SettingsCanvas.pack(side="right")
        self.isSettingsPanelVisible = not self.isSettingsPanelVisible

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y
        print(event.x, event.y)
        self.current_shape = None

    def on_drag(self, event):
        if self.start_x is not None and self.start_y is not None:
            x = event.x
            y = event.y

            if self.current_shape:
                self.MapCanvas.delete(self.current_shape)
            self.current_shape = self.MapCanvas.create_rectangle(self.start_x, self.start_y, x, y, fill=NODE_INNER_COLOR)

    def on_release(self, event):
        self.start_x = None
        self.start_y = None
        self.current_shape = None

def main():
    root = tk.Tk()
    root.title("Custom Canvas Example")
    TopFrame = PathOptimisationFrame(root, width=CANVAS_WIDTH+SIDEBAR_WIDTH, height=CANVAS_HEIGHT, bg="yellow")
    
    TopFrame.pack(padx=0, pady=0)

    root.mainloop()

if __name__ == "__main__":
    main()