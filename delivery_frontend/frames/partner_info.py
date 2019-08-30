import tkinter as tk
import tkinter.ttk as ttk
from request_data import request_partners, request_partner_info


class Partner(tk.Frame):
    def __init__(self, parent, partner, name, pos_x, pos_y, span_x, span_y):
        """
        :parameter: labels: (bool) show the requirement of label of entry
        :parameter: name: whos info is going to showed up
        :return: (list) returns two lists that have information about state
        """
        self.label_frame = tk.LabelFrame(
            parent, text="{} Info".format(name))
        self.label_frame.grid(column=pos_x, row=pos_y, columnspan=span_x,
                              rowspan=span_y, pady=10, padx=10, sticky="NESW")

        # TODO backend method that returns all customers

        self.name_label = tk.Label(
            label_frame, text="{} Name".format(name), font=BASICFONT)
        self.name_label.grid(column=0, row=1, sticky="W")

        self.address_label = tk.Label(
            self.label_frame, text="Address", font=BASICFONT)
        self.address_label.grid(column=0, row=2, sticky="W")

        self.phone_label = tk.Label(
            self.label_frame, text="Phone", font=BASICFONT)
        self.phone_label.grid(column=0, row=3, sticky="W")

        self.contact_label = tk.Label(
            self.label_frame, text="Contact", font=BASICFONT)
        self.contact_label.grid(column=0, row=4, sticky="W")

        # if need lbels than it is going to draw labels, if not draw entries

        self.combobox = ttk.Combobox(
            self.label_frame, values=[], font=ENTRYFONT)
        self.combobox.grid(column=0, row=0, sticky="NESW")
        self.combobox.bind("<<ComboboxSelected>>",
                           lambda: self.update_info(request_partner_info(self.name, self.combobox.get())))

        self.name = tk.Entry(self.label_frame, width=30)
        self.name.grid(column=1, row=1, sticky="NESW")

        self.address = tk.Entry(self.label_frame, width=30)
        self.address.grid(column=1, row=2, sticky="NESW")

        self.phone = tk.Entry(self.label_frame, width=30)
        self.phone.grid(column=1, row=3, sticky="NESW")

        self.contact = tk.Entry(self.label_frame, width=30)
        self.contact.grid(column=1, row=4, sticky="NESW")

        self.entries = {
            "name": self.name,
            "address": self.address,
            "phone": self.phone,
            "contact": self.contact}

    def update_info(self, data_dict):
        self.activate_all()
        if data_dict is None:
            pass
            # probably need to logg this stuff
        else:
            for k, v in self.entries.items():
                v.delete(0, tk.END)
                v.insert(0, data_dictionary[k])
        self.deactivate_all()

    def deactivate_all(self):
        for k, v in self.entries.items():
            v.configure(state="readonly")
        self.combobox.configure(state="disabled")

    def activate_all(self):
        for k, v in self.entries.items():
            v.configure(state="normal")
        self.combobox.configure(state="readonly")

    def update_partners(self, data_list):
        self.activate_all()
        if data is None:
            pass
            # probably need to logg this stuff
        else:
            self.combobox.configure(values=data_list)
        self.deactivate_all()

    def new_partner(self):
        data = {}
        for k, v in self.entries.items():
            data[k] = v
        return data
    self.clear_info()

    def clear_info(self):
        for k, v in self.entries.items():
            v.delete(0, tk.END)
        self.combobox.current(0)
