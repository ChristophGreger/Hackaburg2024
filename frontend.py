import tkinter
from tkinter import ttk


class MyApp(tkinter.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        # Erstellen Sie das Label-Widget
        self.label_text = tkinter.StringVar()
        self.label_text.set("Du wurdest für noch keine Aktivität gematcht!")
        self.label = tkinter.Label(self, textvariable=self.label_text)
        self.label.pack()

        self.tree = ttk.Treeview(self)

        # Definieren Sie die Spalten
        self.tree["columns"] = ("Vorname", "Nachname", "Telefonnummer")

        # Formatieren Sie die Spalten
        self.tree.column("#0", width=0, stretch=tkinter.NO)
        self.tree.column("Vorname", anchor=tkinter.W, width=100)
        self.tree.column("Nachname", anchor=tkinter.W, width=100)
        self.tree.column("Telefonnummer", anchor=tkinter.CENTER, width=100)

        # Erstellen Sie die Spaltenüberschriften
        self.tree.heading("#0", text="", anchor=tkinter.W)
        self.tree.heading("Vorname", text="Vorname", anchor=tkinter.W)
        self.tree.heading("Nachname", text="Nachname", anchor=tkinter.W)
        self.tree.heading("Telefonnummer", text="Telefonnummer", anchor=tkinter.CENTER)

        # Fügen Sie einige Zeilen hinzu
        #self.tree.insert(parent='', index='end', iid=0, text='', values=("Max", "Mustermann", "0123456789"))
        #self.tree.insert(parent='', index='end', iid=1, text='', values=("Erika", "Musterfrau", "9876543210"))

        self.tree.pack(side="top", fill="both", expand=True)

    def matching(self, aktivitat: str, persondict: dict):
        self.label_text.set(f"Du wurdest für die Aktivität {aktivitat} gematcht!")
        self.tree.delete(*self.tree.get_children())
        for i, person in enumerate(persondict):
            self.tree.insert(parent='', index='end', iid=i, text='',
                             values=(person["Vorname"], person["Nachname"], person["Telefonnummer"]))


root = tkinter.Tk()
root.attributes('-fullscreen', True)
app = MyApp(root)
app.mainloop()
