from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
from winlogtimeline.util.logs import Record


class ExportWindow(Toplevel):
    def __init__(self, parent, current_project):
        super().__init__(parent)

        # Class variables
        self.current_project = current_project

        # Window parameters
        self.title('Export Timeline')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Container frame
        self.container = Frame(self)

        # Workspace block
        self.work_container = Frame(self.container)

        # File Name
        self.file_name = StringVar()
        self.file_label = Label(self.work_container, text='Export Name:')
        self.file_path = Entry(self.work_container, width=30, textvariable=self.file_name)

        # File Type
        self.type_label = Label(self.work_container, text='Type:')
        self.type_list = ['- Export File Type -', '.csv <Comma-Separated Vales>']
        self.type_string = StringVar()
        self.type_string.set(self.type_list[0])
        self.type = OptionMenu(self.work_container, self.type_string, *self.type_list, command=self.display_settings)
        self.type.config(width='30')

        self.delimiter_label = Label(self.work_container, text="Delimiter:")
        self.delimiter_list = ['Comma', 'Comma', 'Space', 'Tab']
        self.delimiter_string = StringVar()
        self.delimiter_string.set(self.delimiter_list[0])
        self.delimiter = OptionMenu(self.work_container, self.delimiter_string, *self.delimiter_list)

        self.columns_label = Label(self.work_container, text="Columns to Export:")
        self.columns_names = Record.get_headers()

        self.columns = []
        for c in self.columns_names:
            var = IntVar(value=1)
            self.columns.append([var, Checkbutton(self.work_container, text=c, variable=var)])

        self.filters_var = IntVar(value=0)
        self.filters_checkbutton = Checkbutton(self.work_container, text="Use Current Filter?",
                                               variable=self.filters_var)

        self.cancel_button = Button(self.work_container, text="Cancel", underline=0, command=self.destroy)
        self.export_button = Button(self.work_container, text="Export", underline=0, command=self.export)
        self.bind("<Alt-c>", self.destroy)
        self.bind("<Alt-e>", self.export)

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3
        i = 0

        # Workspace block
        self.file_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.file_path.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.type_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.type.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.delimiter_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.delimiter.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.columns_label.grid(row=i, column=0, padx=padding, sticky='NSW')
        i += 1

        column = 0
        for pair in self.columns:
            pair[1].grid(row=i, column=column, columnspan=1, padx=padding, sticky='NESW')
            column = (column + 1) % 3

            if column == 0:
                i += 1

        # Filter choice isn't actually used right now.
        self.filters_checkbutton.grid(row=i, column=1, columnspan=1, padx=padding, sticky='NESW')
        self.cancel_button.grid(row=i, column=0, padx=padding, pady=padding, sticky='NESW')
        self.export_button.grid(row=i, column=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.work_container.columnconfigure(0, weight=4)
        self.work_container.grid(row=0, column=0, columnspan=5, rowspan=3, sticky='EW')

        self.container.columnconfigure(0, weight=4)
        self.container.pack(fill=BOTH)

        self.delimiter_label.grid_forget()
        self.delimiter.grid_forget()
        self.export_button.config(state=DISABLED)

    def display_settings(self, option):
        """
        Chooses what settings to display based on the choice made in the type dropdown.
        :param option: the option that was selected in the type dropdown. Format = FILE_EXT <FILE_TYPE_NAME>
        """

        padding = 3
        file_extension = option.split(" ")[0]

        if file_extension == ".csv":
            self.delimiter_label.grid(row=2, column=0, padx=padding, sticky='NES')
            self.delimiter.grid(row=2, column=1, columnspan=1, padx=padding, pady=padding, sticky='NESW')
            self.export_button.config(state=NORMAL)

        elif file_extension == ".pdf":
            self.delimiter_label.grid_forget()
            self.delimiter.grid_forget()
            self.export_button.config(state=NORMAL)

    def export(self):
        """
        Starts the export process.
        :return:
        """
        columns = {pair[1].cget("text"): pair[0].get() for pair in self.columns}

        if self.file_path.get() == "":
            messagebox.showerror("Error", "Please provide a valid filename for the exported file.")
            return
        elif '.' in self.file_path.get():
            messagebox.showerror("Error",
                                 "Please provide a valid filename without an extension.\nInstead of '{}' you can use '{}'".format(
                                     self.file_path.get(), self.file_path.get().split(".")[0]))
            return

        type = self.type_string.get().split(" ")[0]
        if type == ".csv":
            self.export_csv(columns)
            return
        elif type == ".pdf":
            self.export_pdf(columns)
            return

    def export_csv(self, columns):
        """
        Exports in csv format
        :param columns:
        :return:
        """
        records = self.current_project.get_all_logs()

        delimiter = None
        if self.delimiter_string.get() == "Comma":
            delimiter = ","
        elif self.delimiter_string.get() == "Space":
            delimiter = " "
        elif self.delimiter_string.get() == "Tab":
            delimiter = "\t"

        from csv import writer

        with open(self.current_project.get_path() + '/{}.csv'.format(self.file_path.get()), 'w') as csvfile:
            w = writer(csvfile, delimiter=delimiter, quoting=0)  # quoting == minimal quoting

            header = [key for key in columns if columns[key] == 1]
            w.writerow(header)

            booleans = [columns[key] for key in columns]

            from itertools import compress
            for r in records:
                values = [r.timestamp_utc, r.event_id, r.description, r.details, r.event_source, r.event_log,
                          r.session_id, r.account, r.computer_name, r.record_number, r.recovered, r.source_file_hash]
                row = list(compress(values, booleans))

                w.writerow(row)

        self.master.master.update_status_bar("Successfully exported timeline in the current project directory!")

        self.destroy()

    def export_pdf(self, columns):
        print("Export .pdf file")
