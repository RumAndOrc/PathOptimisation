import tkinter as tk
from tkinter import messagebox
from PIL import Image,ImageTk 
from vars import *  # type: ignore
import math

def get_leg_id(ids):
        '''
        Creates a unique id for a leg

        - ids is a list of ids
        - Returns "leg_id_invalid" if more than 2 legs in ids, or
        - Returns id in the form "node_id_1<$>node_id_2" where $ is leg difficulty modifier (default zero)
        '''
        if len(ids) !=2:
            print("cautionleg id invalid")
            return "leg_id_invalid"
        num1 =int(ids[0].split('_')[-1])
        num2 =int(ids[1].split('_')[-1])
        print("NUMBNERS:", num1, num2)
        if num1>num2:
            ids = ids[::-1]
            print("FLIPPING")
        return ids[0]+"<0>"+ids[1]
    

class PathOptimisationCanvas(tk.Canvas):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        

class PathOptimisationFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.canvas_map = PathOptimisationCanvas(self, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, bg=CANVAS_BG)# type: ignore
        self.canvas_map.pack(side="left")

        self.is_settings_visible = False
        self.canvas_controls = tk.Canvas(self, width=SIDEBAR_WIDTH, height = CANVAS_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        self.canvas_controls.create_rectangle(SIDEBAR_WIDTH-50, CANVAS_HEIGHT-30, SIDEBAR_WIDTH, CANVAS_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.canvas_controls.tag_bind("btn_settings", "<Button-1>",self.toggle_settings)
        self.canvas_controls.pack(side="right")  

        self.canvas_settings = tk.Canvas(self, width=SIDEBAR_WIDTH, height = CANVAS_HEIGHT, bg = SIDEBAR_BG)# type: ignore
        self.canvas_settings.create_rectangle(SIDEBAR_WIDTH-50, CANVAS_HEIGHT-30, SIDEBAR_WIDTH, CANVAS_HEIGHT, fill="red", tags ="btn_settings")# type: ignore
        self.canvas_settings.tag_bind("btn_settings", "<Button-1>",self.toggle_settings)
        self.canvas_settings.create_text(SIDEBAR_WIDTH/2, 50, text="Settings") # type: ignore

        self.start_x = None
        self.start_y = None
        self.current_shape = None

        self.canvas_map.bind("<Button-2>", self.on_middle_click)
        self.canvas_map.tag_bind("node", "<Button-1>",self.start_create_leg)
        self.canvas_map.tag_bind("node", "<ButtonRelease-1>",self.end_create_leg)
        self.leg_start = None
        self.nodes = {}
        self.legs = []


    def on_middle_click(self, event):
        '''
        Event handler for middle clicking on the map canvas

        -   If an existing node was clicked display a popup 
            warning message asking to confirm delete, then if yes
            call self.remove_node
        -   If a blank space was clicked, call self.create_node
        '''
        node = self.get_node_hit_single(event.x, event.y)
        if (node == None):
            self.create_node(event)
        else:
            result = messagebox.askokcancel("Confirmation", " you are about to delete a node, are you sure?")
            if result:
                self.remove_node(self.get_node_id(node))
            else:
                pass


    def remove_node(self, id):
        '''
        Removes a node and all associated legs

        At present, removes:
            - node circles
            - node dict entry in self.nodes
            - associated leg lines
            - associated leg entries in self.legs
        '''
        del self.nodes[id]
        self.canvas_map.delete(id)
        for leg_num in range(len(self.legs)-1,-1,-1):
            if id in self.legs[leg_num]:
                self.canvas_map.delete("leg_id_"+self.legs[leg_num])
                self.legs.pop(leg_num)
        self.canvas_map.update()


    def create_node(self, event):
        '''
        Creates a new node object (circle on the canvas)

        - Updates the dictionary self.nodes with {node_id : {'x':,'y':}}
        '''
        id = self.get_next_ava_node_id()
        print("Created:",self.canvas_map.create_oval(event.x-(NODE_SIZE/2), event.y-(NODE_SIZE/2), # type: ignore
                                   event.x+(NODE_SIZE/2), event.y+(NODE_SIZE/2), # type: ignore
                                   fill = NODE_INNER_COLOR, # type: ignore
                                   tags = ["node",id]))
        self.nodes.update({id:{'x':event.x, 'y':event.y}})
        return
    

    def get_next_ava_node_id(self):
        '''
        Determines the next unused node id

        IDs are of the form "node_id_$" where $ is an integer starting from zero
        This searches from zero each time so ids previously deleted to be reused
        '''
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
        '''
        Gets the node object id of the node colliding with the x,y provided

        This is mainly used for click events
        - Returns the canvas node(circle) object id if there is only one,
        - If two overlap then returns None
        '''
        all_nodes = self.canvas_map.find_withtag("node")
        hits = self.canvas_map.find_overlapping(x-1, y-1, x+1, y+1)
        target = list(set(all_nodes)&set(hits))
        print("target node[s]:",target)
        if(len(target) == 1):
            return target[0]
        return None


    def start_create_leg(self, event):
        '''
        Starts the leg creation sequence

        If a single node was clicked sets self.leg_start to that object id        
        '''
        self.leg_start = self.get_node_hit_single(event.x, event.y)
        print("start leg:",self.leg_start,self.canvas_map.gettags(self.leg_start))
        return
    

    def get_node_id(self, node):
        '''
        Gets the node id tag from the object provided

        This is mainly used for finding the id of the clicked node
        - returns the node_id 
        '''
        tags = self.canvas_map.gettags(node)
        for tag in tags:
            if "node_id_" in tag:
                return tag

        
    def end_create_leg(self, event):
        '''
        Ends the leg creation sequence

        If the leg has a valid start, and this is a valid end, create a new leg
            - Adds the leg id to self.legs, and
            - Creates a line between the nodes
        '''
        leg_end = self.get_node_hit_single(event.x, event.y)
        if leg_end == None:
            self.leg_start = None
            return
        if self.leg_start != None and leg_end != self.leg_start:
            id_start = self.get_node_id(self.leg_start)
            id_end = self.get_node_id(leg_end)
            leg_id = get_leg_id([id_start, id_end])

            if leg_id in self.legs:
                print("cautuion: leg already exists")
                return
            # below is the trig to make lines start at edges of nodes rather than the centres
            self.legs.append(leg_id)
            x1 = self.nodes[id_start]['x']
            y1 = self.nodes[id_start]['y']
            x2 = self.nodes[id_end]['x']
            y2 = self.nodes[id_end]['y']
            a = abs(float(y1)-y2)/abs(float(x1)-x2)
            xdir = (x2-x1)/abs(x2-x1)
            ydir = (y2-y1)/abs(y2-y1)
            rsq = math.pow((NODE_SIZE/2),2) # type: ignore
            x1diff = math.pow(rsq/(1.0+math.pow(a,2)),0.5) # type: ignore
            y1diff = math.pow(rsq/(1+(1/math.pow(a,2))),0.5)#   ((NODE_SIZE/2)/(1.0+(1.0/math.pow(a,2)))) # type: ignore
            x1 = x1+ xdir * x1diff
            y1 = y1+ ydir * y1diff
            x2 = x2- xdir * x1diff
            y2 = y2- ydir * y1diff
            self.canvas_map.create_line(x1,y1, x2, y2, tags="leg_id_"+leg_id)
        print(self.legs)
        print(self.nodes)
        self.leg_start == None
        return


    def toggle_settings(self, event):
        '''
        Toggles between settings and controls panel on the right side

        - Reads/writes the flag is_settings_visible
        - The two canvases are packed or unpacked (pack_forget)
        '''
        if(self.is_settings_visible):
            self.canvas_settings.pack_forget()
            self.canvas_controls.pack(side="right")
        else:
            self.canvas_controls.pack_forget()
            self.canvas_settings.pack(side="right")
        self.is_settings_visible = not self.is_settings_visible
        return


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