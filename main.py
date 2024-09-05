import tkinter as tk
from puzzle.puzzle import SlidingPuzzle

if __name__ == "__main__":
    root = tk.Tk()
    puzzle = SlidingPuzzle(root)
    root.mainloop()