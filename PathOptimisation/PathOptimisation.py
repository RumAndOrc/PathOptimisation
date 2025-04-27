import tkinter as tk

CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CANVAS_BG = "black"
SIDEBAR_WIDTH = 200
SIDEBAR_HEIGHT = CANVAS_HEIGHT
SIDEBAR_BG = "red"

class PathOptimisationCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
class PathOptimisationFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.MapCanvas = PathOptimisationCanvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BG)
        self.MapCanvas.pack(side="left")
        self.ControlsCanvas = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)
        self.ControlsCanvas.pack(side="right")
        self.bind("<Button-1>", self.on_click)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)

        self.start_x = None
        self.start_y = None
        self.current_shape = None

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
                self.delete(self.current_shape)
            self.current_shape = self.create_rectangle(self.start_x, self.start_y, x, y, fill="blue")

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