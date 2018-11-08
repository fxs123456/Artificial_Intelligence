from tkinter import *
from tkinter.messagebox import *
import random
import layout


class BlockCanvas:
    

    def __init__(self, master, x, y):
        self.clickedNum = 0
        self.WarningImg = PhotoImage(file="./img/warning.png")
        self.x = x
        self.y = y
        self.canvas = Canvas(master, width=27, height=27, bg="gray")
        self.canvas.place(x=x, y=y, anchor=NW)


class Minsweeping:
    def __init__(self, map_width, bombs_num):
        self.clickTimes = 0
        self.MAP_WIDTH = map_width
        self.BOMBS_NUM = bombs_num
        self.unFindBombsNum = self.BOMBS_NUM
        self.BOX_NUM = map_width * map_width
        self.frameWidth = self.MAP_WIDTH * 30 + 40
        self.frameHeight = self.MAP_WIDTH * 30 + 120
        self.root = self.initGameFrame("扫雷雷", self.frameWidth, self.frameHeight)

        self.customButton = Button(self.root, text='自定义', command=self.custom)
        self.customButton.pack(anchor=N, fill=BOTH)

        self.gameMap = self.initMap()
        self.MessageText = {}
        self.setMessageText()
        self.BombImg = PhotoImage(file="./img/BombMini.png")
        self.gameData = self.initGameData()
        self.Blocks = {}
        self.searchList = []

        self.drawDigitsOnSide()
        self.drawBlocks()
        self.root.mainloop()

    def initGameFrame(self, title, width, height):
     
        frame = Tk()
        frame.wm_title(title)
        frame.minsize(width, height)
        frame.maxsize(width, height)
        return frame

    def initMap(self):
    

        map = Canvas(self.root, width=self.MAP_WIDTH * 30 + 40, height=self.MAP_WIDTH * 30 + 90, bg="gray")
        map.create_rectangle(20, 70, self.MAP_WIDTH * 30 + 20, self.MAP_WIDTH * 30 + 70)  # 扫雷的棋盘
        for i in range(0, self.MAP_WIDTH):
            map.create_line(20, 70 + i * 30, self.MAP_WIDTH * 30 + 20, 70 + i * 30)  # 横线
            map.create_line(20 + i * 30, 70, 20 + i * 30, self.MAP_WIDTH * 30 + 70)  # 竖线
        map.pack(anchor=S)
        return map

    def setMessageText(self):
      
        clickTimesmessage = self.gameMap.create_text(self.frameWidth - 50, 30, text="步数：" + str(self.clickTimes))
        unFindBombsMessage = self.gameMap.create_text(20, 30, anchor=W, text="地雷：" + str(self.unFindBombsNum))
        self.MessageText['clickTimesmessage'] = clickTimesmessage
        self.MessageText['unFindBombsMessage'] = unFindBombsMessage

    def drawDigitsOnSide(self):
     
        for i in range(0, self.MAP_WIDTH):
            self.gameMap.create_text(10, 85 + i * 30, text=str(i))
            self.gameMap.create_text(35 + i * 30, 60, text=str(i))

    def initGameData(self):
     
        GameData = {}
        for i in range(0, self.BOX_NUM):
            GameData[str(i)] = 0
        return GameData

    def initBombs(self, passNo):
        BombNos = random.sample(range(0, self.BOX_NUM - 1), self.BOMBS_NUM)
        for i in BombNos:
            if i >= passNo:
                self.gameData[str(i + 1)] = -1
            else:
                self.gameData[str(i)] = -1

    def drawBombs(self):
       
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] == -1:
                x = 20 + 30 * (i % self.MAP_WIDTH)
                y = 70 + 30 * int(i / self.MAP_WIDTH)
                print(str(i) + ": (" + str(i % self.MAP_WIDTH) + ", " + str(int(i / self.MAP_WIDTH)) + ")")
                self.gameMap.create_image(x, y, anchor='nw', image=self.BombImg)

    def drawDigitsAroundBomb(self):
      
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] > 0:
                x = 35 + 30 * (i % self.MAP_WIDTH)
                y = 85 + 30 * int(i / self.MAP_WIDTH)
                self.gameMap.create_text(x, y, text=str(self.gameData[str(i)]))

    def countAllDigits(self):
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] == -1:
                self.countDigitAroundTheBomb(i)

    def countDigitAroundTheBomb(self, bombAddNum):
        if bombAddNum > (self.MAP_WIDTH - 1):
            if bombAddNum < self.MAP_WIDTH * (self.MAP_WIDTH - 1):
                self.countDigitOverBomb(bombAddNum)
                self.countDigitBesideBomb(bombAddNum)
                self.countDigitUnderBomb(bombAddNum)
            else:
                self.countDigitOverBomb(bombAddNum)
                self.countDigitBesideBomb(bombAddNum)
        else:
            self.countDigitBesideBomb(bombAddNum)
            self.countDigitUnderBomb(bombAddNum)

    def countDigitOverBomb(self, bombAddNum):
        if bombAddNum % self.MAP_WIDTH > 0:
            if bombAddNum % self.MAP_WIDTH < (self.MAP_WIDTH - 1):
                for i in range(-1, 2):
                    if self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] >= 0:
                        self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] += 1
            else:
                for i in range(-1, 1):
                    if self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] >= 0:
                        self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] += 1
        else:
            for i in range(0, 2):
                if self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] >= 0:
                    self.gameData[str(bombAddNum - self.MAP_WIDTH + i)] += 1

    def countDigitBesideBomb(self, bombAddNum):
        if bombAddNum % self.MAP_WIDTH > 0:
            if bombAddNum % self.MAP_WIDTH < (self.MAP_WIDTH - 1):
                for i in [-1, 1]:
                    if self.gameData[str(bombAddNum + i)] >= 0:
                        self.gameData[str(bombAddNum + i)] += 1
            else:
                if self.gameData[str(bombAddNum - 1)] >= 0:
                    self.gameData[str(bombAddNum - 1)] += 1
        else:
            if self.gameData[str(bombAddNum + 1)] >= 0:
                self.gameData[str(bombAddNum + 1)] += 1

    def countDigitUnderBomb(self, bombAddNum):
        if bombAddNum % self.MAP_WIDTH > 0:
            if bombAddNum % self.MAP_WIDTH < (self.MAP_WIDTH - 1):
                for i in range(-1, 2):
                    if self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] >= 0:
                        self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] += 1
            else:
                for i in range(-1, 1):
                    if self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] >= 0:
                        self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] += 1
        else:
            for i in range(0, 2):
                if self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] >= 0:
                    self.gameData[str(bombAddNum + self.MAP_WIDTH + i)] += 1

    def drawBlocks(self):
     
        for i in range(0, self.BOX_NUM):
            x = 20 + 30 * (i % self.MAP_WIDTH)
            y = 70 + 30 * int(i / self.MAP_WIDTH)
            theBlock = BlockCanvas(self.gameMap, x, y)
            theBlock.canvas.bind("<Button-1>", self.clickBlock)
            theBlock.canvas.bind("<Button-3>", self.rightClickBlock)
            self.Blocks[str(i)] = theBlock

    def clickBlock(self, event):
        blockBeClicked = event.widget
        if self.clickTimes == 0:
            for i in range(0, self.BOX_NUM):
                if self.Blocks[str(i)].canvas == blockBeClicked:
                    self.initBombs(i)
                    self.drawBombs()
                    self.countAllDigits()
                    self.drawDigitsAroundBomb()
        self.updateClickTimes()
        for i in range(0, self.BOX_NUM):
            if self.Blocks[str(i)].canvas == blockBeClicked:
                px = self.Blocks[str(i)].x
                py = self.Blocks[str(i)].y
                x = int((px - 20) / 30)
                y = int((py - 70) / 30)
                BlockNo = x + y * self.MAP_WIDTH
                self.searchEmptyBox(BlockNo)
                self.isGameWinned()

    def rightClickBlock(self, event):
        blockBeClicked = event.widget
        for i in range(0, self.BOX_NUM):
            if self.Blocks[str(i)].canvas == blockBeClicked:
                self.Blocks[str(i)].clickedNum += 1
                if self.Blocks[str(i)].clickedNum % 2 == 1:
                    self.markBlock(event)
                    self.Blocks[str(i)].canvas.unbind("<Button-1>")
                else:
                    self.deleteMark(event)
                    self.Blocks[str(i)].canvas.bind("<Button-1>", self.clickBlock)

    def markBlock(self, event):
        theBlock = event.widget
        for i in range(0, self.BOX_NUM):
            if self.Blocks[str(i)].canvas == theBlock:
                img = self.Blocks[str(i)].WarningImg
                theBlock.create_image(0, 0, anchor='nw', image=img)
        self.updateUnfindBombsNum(1)

    def deleteMark(self, event):
        theBlock = event.widget
        theBlock.delete(ALL)
        self.updateUnfindBombsNum(-1)

    def updateClickTimes(self):
        self.clickTimes += 1
        text = "步数：" + str(self.clickTimes)
        clickTimesMessage = self.MessageText['clickTimesmessage']
        self.gameMap.itemconfig(clickTimesMessage, text=text)

    def updateUnfindBombsNum(self, i):
        self.unFindBombsNum -= i
        text = "地雷：" + str(self.unFindBombsNum)
        unFindBombsMessage = self.MessageText['unFindBombsMessage']
        self.gameMap.itemconfig(unFindBombsMessage, text=text)

    def searchEmptyBox(self, firstBoxNo):
       
        self.searchList.append(firstBoxNo)
        while self.searchList:
            self.searchTheBox(self.searchList.pop(0))

    def searchTheBox(self, No):
        if self.gameData[str(No)] == 0:
            if No >= self.MAP_WIDTH:
                self.searchUporUnderBoxs(No - self.MAP_WIDTH)
            self.searchBesideBoxs(No)
            if No < self.BOX_NUM - self.MAP_WIDTH - 1:
                self.searchUporUnderBoxs(No + self.MAP_WIDTH)
        self.Blocks[str(No)].canvas.place_forget()
        self.isGameFailed(No)
        self.gameData[str(No)] = -2

    def searchUporUnderBoxs(self, UporDownNo):
        if UporDownNo % self.MAP_WIDTH >= 1:
            if UporDownNo % self.MAP_WIDTH < self.MAP_WIDTH - 1:
                self.searchList.append(UporDownNo - 1)
                self.searchList.append(UporDownNo)
                self.searchList.append(UporDownNo + 1)
            else:
                self.searchList.append(UporDownNo - 1)
                self.searchList.append(UporDownNo)
        else:
            self.searchList.append(UporDownNo)
            self.searchList.append(UporDownNo + 1)

    def searchBesideBoxs(self, No):
        if No % self.MAP_WIDTH >= 1:
            if No % self.MAP_WIDTH < self.MAP_WIDTH - 1:
                self.searchList.append(No - 1)
                self.searchList.append(No + 1)
            else:
                self.searchList.append(No - 1)
        else:
            self.searchList.append(No + 1)

    def isGameFailed(self, blockNo):
       
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] == -1 and blockNo == i:
                self.gameFailed(blockNo)
                self.root.destroy()

    def isGameWinned(self):
       
        blockClickedNum = 0
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] == -2:
                blockClickedNum += 1
        if blockClickedNum == self.BOX_NUM - self.BOMBS_NUM:
            self.gameWinned()
            self.root.destroy()

    def gameFailed(self, No):
        for i in range(0, self.BOX_NUM):
            if self.gameData[str(i)] == -1:
                if i == No:
                    px = self.Blocks[str(i)].x
                    py = self.Blocks[str(i)].y
                    self.gameMap.create_rectangle(px, py, px + 30, py + 30, fill='red')
                    self.gameMap.create_image(px, py, anchor='nw', image=self.BombImg)
                    self.Blocks[str(i)].canvas.place(x=px, y=py, anchor=NW)
                self.Blocks[str(i)].canvas.place_forget()
        showinfo(title="游戏结束！", message="踩到地雷了QwQ")

    def gameWinned(self):
        showinfo(title="游戏结束！", message="恭喜您把地雷都找到了！")

    def custom(self):
        self.root.destroy()
        layout.Layout()


if __name__ == "__main__":
    Minsweeping(10, 10)  
