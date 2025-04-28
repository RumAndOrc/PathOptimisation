import tkinter as tk
from PIL import Image,ImageTk 
from vars import *  # type: ignore


class PathOptimisationCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        

class PathOptimisationFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas_map = PathOptimisationCanvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BG)# type: ignore
        self.canvas_map.pack(side="left")
        #self.MapCanvas.bind("<Button-1>", self.on_click)
        #self.MapCanvas.bind("<B1-Motion>", self.on_drag)
        #self.MapCanvas.bind("<ButtonRelease-1>", self.on_release)
    
        self.is_settings_visible = False
        self.canvas_controls = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        self.canvas_controls.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.canvas_controls.tag_bind("btn_settings", "<Button-1>",self.toggle_settings)
        self.canvas_controls.pack(side="right")  

        self.canvas_settings = tk.Canvas(self, width=SIDEBAR_WIDTH, height = SIDEBAR_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        self.canvas_settings.create_rectangle(SIDEBAR_WIDTH-50, SIDEBAR_HEIGHT-30, SIDEBAR_WIDTH, SIDEBAR_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.canvas_settings.tag_bind("btn_settings", "<Button-1>",self.toggle_settings)
        self.canvas_settings.create_text(SIDEBAR_WIDTH/2, 50, text="Settings") # type: ignore

        self.start_x = None
        self.start_y = None
        self.current_shape = None

        self.canvas_map.bind("<Button-2>", self.create_node)
        self.canvas_map.tag_bind("node", "<Button-1>",self.start_create_leg)
        #self.canvas_map.tag_bind("node", "<ButtonRelease-1>",self.end_create_leg)
        self.leg_start = None
        self.nodes = []


    def create_node(self, event):
        id = self.get_next_ava_node_id()
        print("Created:",self.canvas_map.create_oval(event.x-(NODE_SIZE/2), event.y-(NODE_SIZE/2), # type: ignore
                                   event.x+(NODE_SIZE/2), event.y+(NODE_SIZE/2), # type: ignore
                                   fill = NODE_INNER_COLOR, # type: ignore
                                   tags = ["node",id]))
    

    def get_next_ava_node_id(self):
        valid_id=None
        id = 0
        while(valid_id == None):
            to_try = "node_id_"+str(id)
            if(len(self.canvas_map.find_withtag(to_try))==0):
                valid_id = to_try
            else:
                id+=1
        return valid_id
    

    def get_node_hit_single(self, x,y):
        all_nodes = self.canvas_map.find_withtag("node")
        hits = self.canvas_map.find_overlapping(x-1, y-1, x+1, y+1)
        target = list(set(all_nodes)&set(hits))
        print("target node[s]:",target)
        if(len(target) == 1):
            return target[0]
        else:
            return None

    def start_create_leg(self, event):
        self.leg_start = self.get_node_hit_single(event.x, event.y)
        


    #def end_create_leg(self, event):
        #if(self.leg_start)



    def toggle_settings(self, event):
        if(self.is_settings_visible):
            self.canvas_settings.pack_forget()
            self.canvas_controls.pack(side="right")
        else:
            self.canvas_controls.pack_forget()
            self.canvas_settings.pack(side="right")
        self.is_settings_visible = not self.is_settings_visible


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
                self.canvas_map.delete(self.current_shape)
            self.current_shape = self.canvas_map.create_rectangle(self.start_x, self.start_y, x, y, fill=NODE_INNER_COLOR)# type: ignore


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
def update_settings_file():
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