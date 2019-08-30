import tkinter as tk
import tkinter.ttk as ttk
# import request_data


class Note(tk.Frame):
    def __init__(self, parent, pos_x, pos_y, span_x, span_y):
        self.notes_frame = tk.LabelFrame(parent,
                                         text="Notes")
        self.notes_frame.grid(column=pos_x, row=pos_y,
                              columnspan=span_x, rowspan=span_y, sticky="NESW")
        self.notes = tk.Text(
            self.notes_frame, height=9, width=35, font=ENTRYFONT)

        self.notes.grid(column=0, row=0)

    def deactivate(self):
        self.notes.configure(state="readonly")

    def activate(self):
        self.notes.configure(state="normal")

    def update_notes(self, text):
        self.notes.delete(1.0, tk.END)
        self.notes.insert(1.0, text)

    def clear_notes(self):
        self.notes.delete(1.0, tk.END)

    def read_notes(self):
        return self.notes.get()
