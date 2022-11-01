#!/usr/bin/env python3
#################################################
# Number Labirynth
#
import math
import random
import curses

TABLE    :dict = {}
SOLUTION :list = list(())

scr = curses.initscr()
curses.start_color()
curses.noecho()
curses.cbreak()
scr.keypad(True)
curses.curs_set(False)

# Numbers 1-9 as normal, visited and on route
for i in range(1,10):
    curses.init_pair(i,    i%6+1, 0)
#    curses.init_pair(i+10, i%6+1, curses.COLOR_BLUE)
#    curses.init_pair(i+20, i%6+1, curses.COLOR_GREEN)
# Color of the start and finish
curses.init_pair(10, curses.COLOR_WHITE, curses.COLOR_RED)
# Color of the player
curses.init_pair(20, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(30, curses.COLOR_WHITE, curses.COLOR_WHITE)

#################################################

class Game:

    def __init__(self, SizeX :int =-1, SizeY :int =-1) -> None:
        """Define a new playfield
        Parameters:
        SizeX :int = Horizontal size
        SizeY :int = Vertical size"""

        global TABLE
        self.SizeX :int = SizeX
        self.SizeY :int = SizeY
        self.StrX  :int = SizeX // 6
        self.StrY  :int = SizeY // 6
        self.EndX  :int = SizeX * 5 // 6
        self.EndY  :int = SizeY * 5 // 6

        for j in range(0,self.SizeY):
            for i in range(0,self.SizeX):
                TABLE[str(i)+","+str(j)] = Cell(i,j)
        TABLE[str(self.StrX)+","+str(self.StrY)].makeSpecial()
        TABLE[str(self.EndX)+","+str(self.EndY)].makeSpecial()
        for j in range(0,self.SizeY):
            TABLE["0," + str(j)].allow["L"] = False
            TABLE[str(self.SizeX-1) + "," + str(j)].allow["R"] = False
        for i in range(0,self.SizeX):
            TABLE[str(i) + ",0"].allow["U"] = False
            TABLE[str(i) + "," + str(self.SizeY-1)].allow["D"] = False


    def redrawScreen(self) -> None:
        """Redraw the whole screen"""

        global TABLE
        scr.clear()
        for j in range(0,self.SizeY):
            for i in range(0,self.SizeX):
                TABLE[str(i)+","+str(j)].draw()

    def prettyPrint(self) -> None:
        """For debug purposes, it outputs the actual state of the maze"""
        global TABLE
        CellFace :str =":"
        fpp = open("PrettyPrint.txt","a")
        for j in range(0,self.SizeY):
            for i in range(0,self.SizeX):
                cObj = TABLE[str(i)+","+str(j)]
                if cObj.allow["U"] :
                    fpp.write("# #")
                else :
                    fpp.write("###")
            fpp.write("\n")
            for i in range(0, self.SizeX):
                cObj = TABLE[str(i)+","+str(j)]
                #CellFace = "x" if len(cObj.MyRoute) else ":"
                CellFace = str(len(cObj.MyRoute))[-1]
                if i == self.StrX and j == self.StrY : CellFace = "S"
                if i == self.EndX and j == self.EndY : CellFace = "E"
                if cObj.allow["L"]:
                    fpp.write(" "+CellFace)
                else:
                    fpp.write("#"+CellFace)
                if cObj.allow["R"]:
                    fpp.write(" ")
                else:
                    fpp.write("#")
            fpp.write("\n")
            for i in range(0, self.SizeX):
                cObj = TABLE[str(i)+","+str(j)]
                if cObj.allow["D"]:
                    fpp.write("# #")
                else:
                    fpp.write("###")
            fpp.write("\n")
        fpp.write("\n\n\n")
        fpp.close()



class Cell:

    def __init__(self, X :int =-1, Y :int =-1, Val :int =-1) -> None:
        """Define one cell element
        Parameters:
        X :int = X coordinate of the cell
        Y :int = Y coordinate of the cell
        Val :int = Intial value of the cell (0-9) / if omitted: will be random generated"""

        self.X   :int = X
        self.Y   :int = Y
        self.Val :int = Val
        self.Visited :bool =False
        self.Route   :bool =False
        self.Special :bool =False
        self.allow   :dict ={"U":True, "D":True, "L":True, "R":True}
        self.MyRoute :list =list(())
        # For debug purposes only
        self.IamSolution :bool =False

        if self.Val < 0: self.Val = random.randint(1, 9)


    def draw(self) -> None:
        """Draw the character to the current cursor position"""
        col :int = curses.color_pair(self.Val)
        if self.Route:   col = curses.color_pair(30) | curses.A_BOLD
        if self.Visited: col = col | curses.A_REVERSE
        if self.Special:
            scr.addstr(self.Y, self.X, str(self.Val), curses.color_pair(10) | curses.A_BOLD)
        else:
            scr.addstr(self.Y, self.X, str(self.Val), col)

    def visit(self) -> None:
        """Trigger the visited flag"""
        self.Visited = True

    def onroute(self) -> None:
        """Define the cell being on the final route"""
        self.Route = True

    def offroute(self) -> None:
        """Remove the cell from the route"""
        self.Route = False

    def makeSpecial(self) -> None:
        """Change it to a special cell (start or finish)"""
        self.Special = True

    def tailYourself(self, OList) -> None:
        """Generate my own route list by appending myself to the received list
        Parameters:
        OList :list = List of Cellobjects so far"""
        for xxx in OList : self.MyRoute.append(xxx)
        self.MyRoute.append(self)

    def makeSolution(self) -> None:
        """Make myself part of the solution"""
        self.IamSolution = True


class Player:

    def __init__(self, PosX :int =-1, PosY :int =-1) -> None:
        """Initialize a player with a given position and empty route
        Parameters:
        PosX :int = Horizontal position
        PosY :int = Vertical position"""
        self.X :int = PosX
        self.Y :int = PosY
        self.Route :list = list(())
        self.Won :bool =False


    def draw(self) -> None:
        """Draw the player to its appropriate position"""
        scr.addstr(self.Y, self.X, "@", curses.color_pair(20) | curses.A_BOLD)


    def step(self, Dir :str ="") -> None:
        """Try to step with the player into a certain direction
        Parameters:
        Dir :str = Stepping direction [U/D/L/R or N/S/W/E]"""

        global TABLE
        newX :int = self.X
        newY :int = self.Y
        currCell = TABLE[str(newX)+","+str(newY)]

        # apply direction
        if Dir.upper() in {"N","U"}: newY -= 1
        if Dir.upper() in {"S","D"}: newY += 1
        if Dir.upper() in {"W","L"}: newX -= 1
        if Dir.upper() in {"E","R"}: newX += 1

        # check if playfield limimts are reached
        if newX >= g.SizeX or newX < 0 or newY >= g.SizeY or newY < 0 : return

        # check if value makes it possible to step
        newCell = TABLE[str(newX)+","+str(newY)]
        if newCell.Val - currCell.Val not in {1, -1} : return

        # check if we are stepping on a cell with route, if yes then trim to the previous cell
        if newCell.Route :
            idx = self.Route.index(newCell)
            for id2 in range(idx, len(self.Route)) : self.Route[id2].offroute()
            self.Route = self.Route[0:idx]

        # mark current cell as visited and put new cell on the route
        currCell.visit()
        newCell.onroute()
        p.Route.append(newCell)

        # step and check if won
        self.X , self.Y = newX , newY
        if self.X == g.EndX and self.Y == g.EndY : self.Won = True



#################################################

def recurGenWalls(L: int, T: int, R: int, B: int) -> None:
    """Recursively generate walls by splitting the free rectangled areas
    Parameters:
    L :int = Leftmost cell of the area
    T :int = Top cell of the area
    R :int = Rightmost cell of the area
    B :int = Bottom cell of the area"""

    global TABLE

    Wid :int = abs(R-L+1)
    Hei :int = abs(B-T+1)
    if Wid == 1 or Hei == 1 : return

    if Wid >= Hei:
        splitX :int = random.randint(L, R-1)
        splitY :int = random.randint(T, B)
        for j in range(T, B+1):
            if j != splitY:
                TABLE[str(splitX)  +","+str(j)].allow["R"] = False
                TABLE[str(splitX+1)+","+str(j)].allow["L"] = False
        recurGenWalls(L, T, splitX, B)
        recurGenWalls(splitX+1, T, R, B)
    else:
        splitY :int = random.randint(T, B-1)
        splitX :int = random.randint(L, R)
        for i in range(L, R+1):
            if i != splitX:
                TABLE[str(i)+","+str(splitY)].allow["D"] = False
                TABLE[str(i)+","+str(splitY+1)].allow["U"] = False
        recurGenWalls(L, T, R, splitY)
        recurGenWalls(L, splitY+1, R, B)



#################################################


# Generate map, initialize start and end, place player to the start
g = Game(60,30)
recurGenWalls(0,0,59,29)

TABLE[str(g.StrX)+","+str(g.StrY)].MyRoute.append(TABLE[str(g.StrX)+","+str(g.StrY)])

# Scan through all cells and update personal route
WasChange :bool =True
while WasChange:
    WasChange =False
    for j in range(0,g.SizeY):
        for i in range(0,g.SizeX):
            o1 = TABLE[str(i)+","+str(j)]
            if len(o1.MyRoute):
                if o1.allow["L"] and not len(TABLE[str(i-1)+","+str(j)].MyRoute):
                    TABLE[str(i-1)+","+str(j)].tailYourself(o1.MyRoute)
                    WasChange = True
                if o1.allow["R"] and not len(TABLE[str(i+1)+","+str(j)].MyRoute):
                    TABLE[str(i+1)+","+str(j)].tailYourself(o1.MyRoute)
                    WasChange = True
                if o1.allow["U"] and not len(TABLE[str(i)+","+str(j-1)].MyRoute):
                    TABLE[str(i)+","+str(j-1)].tailYourself(o1.MyRoute)
                    WasChange = True
                if o1.allow["D"] and not len(TABLE[str(i)+","+str(j+1)].MyRoute):
                    TABLE[str(i)+","+str(j+1)].tailYourself(o1.MyRoute)
                    WasChange = True
    #--- For debug purposes only
    #g.prettyPrint()
    #***
SOLUTION = TABLE[str(g.EndX)+","+str(g.EndY)].MyRoute

# Generate an own number list for the route
ValList :list =list(())
CurValue :int = random.randint(1,9)
ValTarget :int = random.randint(1,9)
while len(ValList) < len(SOLUTION):
    ValList.append(CurValue)
    while ValTarget == CurValue : ValTarget = random.randint(1, 9)
    if ValTarget > CurValue:
        CurValue+=1
    else:
        CurValue-=1
for i in range(0, len(SOLUTION)) : SOLUTION[i].Val = ValList[i]

#--- For debug purposes only
#fdbg = open("debug.txt","w")
#fdbg.write(str(ValList)+"\n\n")
#fdbg.write((str(len(SOLUTION)))+"   "+str(len(ValList))+"\n\n\n")
#for o2 in SOLUTION:
#    fdbg.write(str(o2.X)+"\t"+str(o2.Y)+"\n")
#    o2.makeSolution()
#fdbg.close()
#***

p = Player(g.StrX,g.StrY)
p.Route.append(TABLE[str(g.StrX)+","+str(g.StrY)])
scr.clear()

# Main loop
while not p.Won:
    g.redrawScreen()
    p.draw()
    scr.addstr(g.SizeY+1, 0,"["+str(TABLE[str(p.X)+","+str(p.Y)].Val)+"] >", curses.color_pair(20))
    scr.refresh()
    cmd = scr.getch()

    if cmd == ord('q'): break
    if cmd == curses.KEY_UP:    p.step("U")
    if cmd == curses.KEY_DOWN:  p.step("D")
    if cmd == curses.KEY_LEFT:  p.step("L")
    if cmd == curses.KEY_RIGHT: p.step("R")

if p.Won :
    scr.addstr(10, 10, "             ")
    scr.addstr(11, 10, "  YOU WON !  ", curses.color_pair(20) | curses.A_BOLD)
    scr.addstr(12, 10, "             ")
    scr.refresh()
    scr.getkey()


curses.curs_set(True)
scr.keypad(False)
curses.cbreak()
curses.echo()
curses.endwin()
