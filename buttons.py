import tkinter as tk

class MainGUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Hello, world!")
        label.pack(fill="both", expand=True, padx=20, pady=20)

class Popup(tk.Toplevel):
    def __init__(self, root):
        tk.Toplevel.__init__(self, root)
        label = tk.Label(self, text="Click to continue...")
        label.pack(fill="both", expand=True, padx=20, pady=20)

        button = tk.Button(self, text="OK", command=self.destroy)
        button.pack(side="bottom")

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    popup = Popup(root)
    root.wait_window(popup)

    main = MainGUI(root)
    main.pack(fill="both", expand=True)

    root.deiconify()
    root.mainloop()