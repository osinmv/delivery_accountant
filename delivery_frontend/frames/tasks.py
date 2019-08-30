import tkinter as tk
import tkinter.ttk as ttk


class Tasks(tk.Frame):

    def __init__(self, parent, length, pos_x, pos_y, span_x, span_y):
        """
        draws tasks in this format Task:
            goal(string)  |  checkbox(bool)  |  target date(date)
        :parameter: length: (integer) tells how any tasks to draw

        """
        self.tasks = []
        self.label_frame_tasks = tk.LabelFrame(parent,
                                               text="Tasks")
        self.label_frame_tasks.grid(
            column=pos_x, row=pos_y, columnspan=span_x,
            rowspan=span_y, padx=10, pady=10)
        self.task_label = tk.Label(self.label_frame_tasks, text="Tasks")
        self.task_label.grid(column=0, row=0)
        self.done_label = tk.Label(self.label_frame_tasks, text="Done")
        self.done_label.grid(column=1, row=0)
        self.task_date_label = tk.Label(self.label_frame_tasks, text="Date")
        self.task_date_label.grid(column=2, row=0)
        self.task_date_must_label = tk.Label(
            self.label_frame_tasks, text="Must Date")
        self.task_date_must_label.grid(column=3, row=0)
        for i in range(0, length):
            entry = tk.Entry(self.label_frame_tasks, width="75")
            entry.grid(column=0, row=i+1)

            check = tk.BooleanVar()
            check_button = tk.Checkbutton(self.label_frame_tasks, var=check)
            check_button.grid(column=1, row=i+1)

            date = DateEntry(self.label_frame_tasks, width="25")
            date.grid(column=2, row=i+1)
            date.configure(state="readonly")
            date_must = DateEntry(self.label_frame_tasks, width="25")
            date_must.grid(column=3, row=i+1)
            date_must.configure(state="readonly")
            self.tasks.append({
                "text": entry,
                "done": check,
                "date": date,
                "data_must": date_must
                "check_button": check_button
            })

    def update_tasks(self, data_dict):
        for num, obj in enumerate(data_dict):
            self.tasks[i]["text"].delete(0, tk.END)
            self.tasks[i]["text"].insert(0, obj["text"])
            self.tasks[i]["done"].set(obj["done"])
            self.tasks[i]["date"].delete(0, tk.END)
            self.tasks[i]["date"].insert(0, obj["date"])
            self.tasks[i]["date_must"].delete(0, tk.END)
            self.tasks[i]["date_must"].insert(0, obj["date_must"])

    def clear_all(self):
        for i in self.tasks:
            i["text"].delete(0, tk.END)
            i["done"].set(False)
            i["date"].delete(0, tk.END)
            i["date_must"].delete(0, tk.END)

    def activate_all(self):
        for i in self.tasks:
            i["text"].configure(state="normal")
            i["date"].configure(state="normal")
            i["date_must"].configure(state="normal")
            i["check_button"].configure(state="normal")

    def deactivate_all(self):
        for i in self.tasks:
            text = i["text"].get()
            if not text and not text.isspace() and text is not None:
                i["text"].configure(state="readonly")
                i["date"].configure(state="readonly")
                i["date_must"].configure(state="readonly")
                if not i["done"]:
                    i["check_button"].configure(state="normal")
                else:
                    i["check_button"].configure(state="readonly")

    def read_tasks(self):
        data = {}
        for num, obj in enumerate(self.tasks):
            data[str(num)] = {
                "text": obj["text"].get(),
                "done": obj["done"].get()
                "date": "20"+obj["date"].get()
                "date_must": obj["date_must"].delete(0, tk.END)}
