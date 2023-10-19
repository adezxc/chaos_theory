import tkinter as tk
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

class App(tk.Frame):
    def __init__( self, parent):
        tk.Frame.__init__(self, parent)
        self._createVariables(parent)
        self._createButton()
        self._createCanvas()
        self._createCanvasBinding()

    def _createButton(self):
        self.button = tk.Button(self.parent, text="Choose image", command=self._openImage)
        self.button.grid(row=1, column=0, sticky='w')

    def _openImage(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor='nw', image=self.photo)
            self.parent.geometry(f"{self.image.width}x{self.image.height + 100}")
            self.canvas.config(width=self.image.width, height=self.image.height)

    def _createVariables(self, parent):
        self.parent = parent
        self.rectx0 = 0
        self.recty0 = 0
        self.rectx1 = 0
        self.recty1 = 0
        self.rectid = None
        self.brightnessList = []

    def _createCanvas(self):
        self.canvas = tk.Canvas(self.parent, 
                                bg = "white" )
        self.canvas.grid(row=2, column=0, sticky='nsew')

    def _createCanvasBinding(self):
        self.canvas.bind( "<Button-1>", self.startRect )
        self.canvas.bind( "<ButtonRelease-1>", self.stopRect )
        self.canvas.bind( "<B1-Motion>", self.movingRect )

    def startRect(self, event):
        self.canvas.delete("rectangles")
        
        self.rectx0 = self.canvas.canvasx(event.x)
        self.recty0 = self.canvas.canvasy(event.y) 
        self.rectid = self.canvas.create_rectangle(
            self.rectx0, self.recty0, self.rectx0, self.recty0, tags='rectangles')

    def movingRect(self, event):
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectid, self.rectx0, self.recty0,
                      self.rectx1, self.recty1)

    def stopRect(self, event):
        for rect in self.canvas.find_withtag("rectangle"):
            if rect != self.rectid:
                self.canvas.delete(rect)
        
        self.rectx1 = self.canvas.canvasx(event.x)
        self.recty1 = self.canvas.canvasy(event.y)
        self.canvas.coords(self.rectid, self.rectx0, self.recty0, self.rectx1, self.recty1)
        self.renderGraph()

    def renderGraph(self):
        if self.rectx1 < self.rectx0:
            self.rectx1, self.rectx0 = self.rectx0, self.rectx1
        if self.recty1 < self.recty0:
            self.recty1, self.recty0 = self.recty0, self.recty1
        cropped_image = self.image.crop((self.rectx0, self.recty0, self.rectx1, self.recty1))
        image_array = np.array(cropped_image)
        height, width = image_array.shape[0], image_array.shape[1]

        # Split the image into 3x3 squares
        square_size = 3
        squares = []
        for i in range(0, height, square_size):
            for j in range(0, width, square_size):
                square = image_array[i:i+square_size, j:j+square_size]
                squares.append(square)
        average_values = []
        for square in squares:
            average_value = np.mean(square)
            average_values.append(average_value)

        x = range(len(average_values))
        y = average_values
        plt.plot(x, y)
        plt.xlabel('Square Number')
        plt.ylabel('Average Color')
        plt.title('Average Color for Each Square')
        plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry( "600x400" )
    app = App(root)
    root.mainloop()
