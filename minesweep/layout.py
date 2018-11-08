from tkinter import *
from tkinter.messagebox import *
import minesweep


class Layout:
    def __init__(self):
        self.MAP_WIDTH = 10
        self.BOMBS_NUM = 10
        self.frame = Tk()
        self.frame.minsize(300, 200)
        self.frame.title('layout')
        self.createWights()
        self.frame.mainloop()

    def createWights(self):
        selectLabelFrame = LabelFrame(self.frame, text="请自定义地图宽度和地雷数：")
        selectLabelFrame.pack(expand=YES)
        width_label = Label(selectLabelFrame, text='地图宽度')
        bombs_label = Label(selectLabelFrame, text='地雷数')
        self.width_input = Entry(selectLabelFrame)
        self.bombs_input = Entry(selectLabelFrame)
        determineButton = Button(selectLabelFrame, text="确认", command=self.determine)
        width_label.pack()
        self.width_input.pack()
        bombs_label.pack()
        self.bombs_input.pack()
        determineButton.pack()

    def determine(self):
        self.MAP_WIDTH = int(self.width_input.get())
        self.BOMBS_NUM = int(self.bombs_input.get())
        self.frame.destroy()
        minesweep.Minsweeping(self.MAP_WIDTH, self.BOMBS_NUM)


if __name__ == '__main__':
    Layout()
