import tkinter as tk

from PIL import Image,ImageTk 

from vars import *  # type: ignore

class PathOptimisationCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
class PathOptimisationFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.MapCanvas = PathOptimisationCanvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BG)# type: ignore
        self.MapCanvas.pack(side="left")
        self.MapCanvas.bind("<Button-1>", self.on_click)
        self.MapCanvas.bind("<B1-Motion>", self.on_drag)
        self.MapCanvas.bind("<ButtonRelease-1>", self.on_release)

        self.isSettingsPanelVisible = False
        self.ControlsCanvas = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        btn_settings = self.ControlsCanvas.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.ControlsCanvas.tag_bind(btn_settings, "<Button-1>",self.swapToSettings)
        self.ControlsCanvas.pack(side="right")  

        self.SettingsCanvas = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        btn_Settings = self.SettingsCanvas.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.SettingsCanvas.tag_bind(btn_settings, "<Button-1>",self.swapToSettings)
        self.SettingsCanvas.create_text(SIDEBAR_WIDTH/2, 50, text="Settings") # type: ignore

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
            self.current_shape = self.MapCanvas.create_rectangle(self.start_x, self.start_y, x, y, fill=NODE_INNER_COLOR)# type: ignore

    def on_release(self, event):
        self.start_x = None
        self.start_y = None
        self.current_shape = None

def main():
    root = tk.Tk()
    root.title("Custom Canvas Example")
    TopFrame = PathOptimisationFrame(root, width=CANVAS_WIDTH+SIDEBAR_WIDTH, height=CANVAS_HEIGHT, bg="yellow")# type: ignore
    
    TopFrame.pack(padx=0, pady=0)

    root.mainloop()


'''
    TODO
    For updating settings to 'vars.py' file
'''
def updateSettingsFile():
    file = open("vars.py", 'r')
    for line in file:
        print(line)
    """
    NODE_INNER_COLOR="purple"
    CANVAS_BG="grey"
    SIDEBAR_BG="brown"
    CONNECTOR_COLOR = "black"
    CONNECTOR_EASY_COLOR = "blue"
    CONNECTOR_HARD_COLOR = "red"
    """
    file.close

if __name__ == "__main__":
    
    main()