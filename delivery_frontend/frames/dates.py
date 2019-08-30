import tkinter as tk
import tkinter.ttk as ttk


class Date(tk.Frame):
    def __init__(self, parent, pos_x, pos_y, span_x, span_y):
        self.label_frame_dates = tk.LabelFrame(parent,
                                               text="About Dates")
        self.label_frame_dates.grid(
            column=pos_x, row=pos_y, columnspan=span_x,
            rowspan=span_y, padx=10, pady=10, sticky="NEW")

        self.date_client = tk.Label(
            self.label_frame_dates, text="Client", font=BASICFONT)
        self.date_client.grid(column=0, row=0, sticky="W")
        self.date_requested = tk.Label(
            self.label_frame_dates, text="Requested", font=BASICFONT)
        self.date_requested.grid(column=0, row=1, sticky="w")
        self.date_ship = tk.Label(
            self.label_frame_dates, text="Shipment", font=BASICFONT)
        self.date_ship.grid(column=0, row=2, sticky="w")

        self.entry_client = DateEntry(
            self.label_frame_dates, font=ENTRYFONT)
        self.entry_client.grid(column=1, row=0, sticky="w")

        self.entry_requested = DateEntry(
            self.label_frame_dates, font=ENTRYFONT)
        self.entry_requested.grid(column=1, row=1, sticky="w")

        self.entry_ship = DateEntry(self.label_frame_dates, font=ENTRYFONT)
        self.entry_ship.grid(column=1, row=2, sticky="w")

        self.entries = {
            "date_client": self.entry_client,
            "date_requested": self.entry_requested,
            "date_shipment": self.entry_ships
        }

    def update_dates(self, data_dict):
        self.activate_all()
        if data_dict is None:
            pass
        else
        for k, v in self.entries.items():
            v.delete(0, tk.END)
            v.insert(0, data_dict[k])
        self.deactivate_all()

    def clear_dates(self):
        self.activate_all()
        for k, v in self.entries.items():
            v.delete(0, tk.END)
        self.deactivate_all()

    def deactivate_all(self):
        for k, v in self.entries.items():
            v.configure(state="readonly")

    def activate_all(self):
        for k, v in self.entries.items():
            v.configure(state="normal")

    def read_date(self):
        data = {}
        self.activate_all()
        for k, v in self.entries.items():
            data[k] = v.get()
        self.deactivate_all()
        return data