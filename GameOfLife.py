import tkinter as tk


class LifeGame:
    def __init__(self, rules, height, width, canvas):
        self.board = [[False for _ in range(height)] for _ in range(width)]
        self.rules = rules
        self.speed = 1
        self.running = False
        self.canvas = canvas

    def clickingCell(self, event):
        # Obsługuje kliknięcie komórki na planszy gry
        cellSize = 20
        row = event.y // cellSize
        col = event.x // cellSize
        self.board[row][col] = not self.board[row][col]
        self.drawBoard()

    def drawBoard(self):
        # Rysuje stan planszy gry na płótnie
        cellSize = 20
        self.canvas.delete("all")
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                x = j * cellSize
                y = i * cellSize
                if self.board[i][j]:
                    self.canvas.create_rectangle(x, y, x + cellSize, y + cellSize, fill="black")
                else:
                    self.canvas.create_rectangle(x, y, x + cellSize, y + cellSize, fill="white")

    def startGame(self):
        # Rozpoczyna grę, uruchamiając pętlę gry
        if not self.running:
            self.running = True
            self.nextStep()

    def stopGame(self):
        # Zatrzymuje grę
        self.running = False

    def nextStep(self):
        # Oblicza i wyświetla następny krok w grze
        if self.running:
            self.calculateNextStep()
            self.drawBoard()
            root.after(int(1000 / self.speed), self.nextStep)

    def calculateNextStep(self):
        # Oblicza następny krok w grze na podstawie aktualnego stanu planszy i zasad
        stayAlive = [int(digit) for digit in self.rules.split("/")[0]]
        becomeAlive = [int(digit) for digit in self.rules.split("/")[1]]
        newBoard = [[False for _ in range(len(self.board[0]))] for _ in range(len(self.board))]
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if not self.board[i][j]:
                    tmp = False
                    for digit in becomeAlive:
                        if self.countNeighbours(i, j) == digit:
                            tmp = True
                    newBoard[i][j] = tmp
                else:
                    tmp = False
                    for digit in stayAlive:
                        if self.countNeighbours(i, j) == digit:
                            tmp = True
                    newBoard[i][j] = tmp
        self.board = newBoard

    def countNeighbours(self, a, b):
        # Liczy liczbę żywych sąsiadów dla danej komórki
        neighbours = 0
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                if self.pointAlive(a + i, b + j):
                    neighbours += 1
        return neighbours

    def pointAlive(self, a, b):
        # Liczy liczbę żywych sąsiadów dla danej komórki
        if a < 0 or a >= len(self.board) or b < 0 or b >= len(self.board[0]):
            return False
        return self.board[a][b]

    def updateSpeed(self, value):
        # Aktualizuje prędkość gry na podstawie wybranej opcji z menu prędkości
        self.speed = float(value)


def start():
    # Rozpoczyna grę na podstawie wprowadzonych parametrów
    cellSize = 20
    rules = rulesEntry.get()
    height = int(heightEntry.get())
    width = int(widthEntry.get())

    rulesLabel.pack_forget()
    rulesEntry.pack_forget()
    heightLabel.pack_forget()
    heightEntry.pack_forget()
    widthLabel.pack_forget()
    widthEntry.pack_forget()
    startButton.pack_forget()

    gameFrame = tk.Frame(root)
    gameFrame.pack()

    canvas = tk.Canvas(gameFrame, width=width * cellSize, height=height * cellSize)
    canvas.pack()

    life_game = LifeGame(rules, height, width, canvas)

    cellSize = 20

    canvas.bind("<Button-1>", life_game.clickingCell)

    start_button = tk.Button(gameFrame, text="Start", command=life_game.startGame)
    start_button.pack(side=tk.LEFT)

    stop_button = tk.Button(gameFrame, text="Stop", command=life_game.stopGame)
    stop_button.pack(side=tk.LEFT)
    speed_var = tk.StringVar(root)
    speed_var.set("1")
    speed_label = tk.Label(gameFrame, text="Speed:")
    speed_label.pack(side=tk.LEFT)
    speed_option_menu = tk.OptionMenu(gameFrame, speed_var, "0.25", "0.5", "1", "2", "4", "8", "16", command=life_game.updateSpeed)
    speed_option_menu.pack(side=tk.LEFT)

    def drawBoardGUI():
        # Rysuje stan planszy gry na płótnie
        canvas.delete("all")
        for i in range(len(life_game.board)):
            for j in range(len(life_game.board[0])):
                x = j * cellSize
                y = i * cellSize
                if life_game.board[i][j]:
                    canvas.create_rectangle(x, y, x + cellSize, y + cellSize, fill="black")
                else:
                    canvas.create_rectangle(x, y, x + cellSize, y + cellSize, fill="white")

    drawBoardGUI()
    return canvas


root = tk.Tk()
root.resizable(False, False)
root.title("The game of life")
rulesLabel = tk.Label(root, text="Rules:")
rulesLabel.pack()
rulesEntry = tk.Entry(root)
rulesEntry.pack()
rulesEntry.insert(tk.END, "23/3")

heightLabel = tk.Label(root, text="Height:")
heightLabel.pack()
heightEntry = tk.Entry(root)
heightEntry.pack()
heightEntry.insert(tk.END, "20")

widthLabel = tk.Label(root, text="Width:")
widthLabel.pack()
widthEntry = tk.Entry(root)
widthEntry.pack()
widthEntry.insert(tk.END, "20")

startButton = tk.Button(root, text="Start Game", command=start)
startButton.pack()

root.mainloop()
