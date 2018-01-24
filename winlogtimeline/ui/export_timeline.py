from tkinter import *
from tkinter import filedialog, messagebox
from tkinter.ttk import *
from winlogtimeline.util.logs import Record
import os
from csv import writer
from itertools import compress


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
        self.file_name.trace('w', lambda *args: self.callback_update_path())
        self.file_label = Label(self.work_container, text='File Name:')
        self.file_entry = Entry(self.work_container, textvariable=self.file_name)

        self.path_name = StringVar()
        self.path_name.set(os.path.abspath(self.current_project.get_path()))
        self.path_label = Label(self.work_container, text='File Path:')
        self.path_entry = Entry(self.work_container, textvariable=self.path_name)
        self.path_button = Button(self.work_container, width=3, text='...', command=self.callback_path_prompt)

        self.file_overwrite = Label(self.work_container, text='Warning:')

        # File Type
        self.type_label = Label(self.work_container, text='Type:')
        self.type_list = ['.csv <Comma-Separated Vales>', '.csv <Comma-Separated Vales>']
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
        self.file_label.grid(row=i, column=0, columnspan=1, padx=padding, sticky='NES')
        self.file_entry.grid(row=i, column=1, columnspan=4, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.path_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.path_entry.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        self.path_button.grid(row=i, column=4, columnspan=1, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.overwrite_row = i
        self.file_overwrite.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NEW')
        i += 1

        self.type_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.type.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        self.delimiter_row = i
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
        self.work_container.grid(row=0, column=0, columnspan=5, rowspan=12, sticky='NW')

        self.container.columnconfigure(0, weight=4)
        self.container.pack(fill=BOTH)

        self.file_overwrite.grid_forget()
        self.export_button.config(state=DISABLED)

    def display_settings(self, option):
        """
        Chooses what settings to display based on the choice made in the type dropdown.
        :param option: the option that was selected in the type dropdown. Format = FILE_EXT <FILE_TYPE_NAME>
        """

        padding = 3
        file_extension = option.split(" ")[0]

        if file_extension == ".csv":
            self.delimiter_label.grid(row=self.delimiter_row, column=0, padx=padding, sticky='NES')
            self.delimiter.grid(row=self.delimiter_row, column=1, columnspan=1, padx=padding, pady=padding,
                                sticky='NESW')

        elif file_extension == ".pdf":
            self.delimiter_label.grid_forget()
            self.delimiter.grid_forget()

    def callback_path_prompt(self):
        """
        Callback used to kick off a directory selection prompt.
        :return:
        """
        workspace = filedialog.askdirectory()
        if len(workspace) > 0:
            self.path_name.set(os.path.abspath(workspace))

        file_type = self.type_string.get().split(" ")[0]
        self.file = os.path.join(os.path.abspath(self.path_name.get()),
                                 self.file_name.get() + file_type)
        if os.path.isfile(self.file):
            self.file_overwrite.grid(row=self.overwrite_row, column=0, columnspan=5, padx=3, pady=3, sticky='NESW')
            self.file_overwrite.config(
                text="Warning: A file named '{}{}' at the current location already exists.\nIt may be overwritten.".format(
                    self.file_name.get(), file_type), foreground="red", anchor=CENTER)
        else:
            self.file_overwrite.grid_forget()

    def callback_update_path(self):
        """
        Callback used when either the workspace or title entry widgets are modified. Updates the value of the path entry
        widget.
        :return:
        """
        file_type = self.type_string.get().split(" ")[0]
        # Update the project path and ensure that the path is valid.
        self.file = os.path.join(os.path.abspath(self.path_name.get()), self.file_name.get() + file_type)

        if os.path.isfile(self.file):
            self.file_overwrite.grid(row=self.overwrite_row, column=0, columnspan=5, padx=3, pady=3, sticky='NESW')
            self.file_overwrite.config(
                text="Warning: A file named '{}{}' at the current location already exists.\nIt may be overwritten.".format(
                    self.file_name.get(), file_type), foreground="red", anchor=CENTER)
        else:
            self.file_overwrite.grid_forget()

        if len(self.file_name.get()) > 0:
            self.export_button.config(state=NORMAL)
        else:
            self.export_button.config(state=DISABLED)

    def export(self):
        """
        Starts the export process.
        :return:
        """
        columns = {pair[1].cget("text"): pair[0].get() for pair in self.columns}

        if self.file_name.get() == "":
            messagebox.showerror("Error", "Please provide a valid filename for the exported file.")
            return
        elif '.' in self.file_name.get():
            messagebox.showerror("Error",
                                 "Please provide a valid filename without an extension.\nInstead of '{}' you can use '{}'".format(
                                     self.file_name.get(), self.file_name.get().split(".")[0]))
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

        with open(self.file, 'w') as csvfile:
            w = writer(csvfile, delimiter=delimiter, quoting=0)  # quoting == minimal quoting

            header = [key for key in columns if columns[key] == 1]
            w.writerow(header)

            booleans = [columns[key] for key in columns]

            for r in records:
                values = [r.timestamp_utc, r.event_id, r.description, r.details, r.event_source, r.event_log,
                          r.session_id, r.account, r.computer_name, r.record_number, r.recovered, r.source_file_alias]
                row = list(compress(values, booleans))

                w.writerow(row)

        self.master.master.update_status_bar("Successfully exported timeline to {}".format(self.file))

        self.destroy()

    def export_pdf(self, columns):
        print("Export .pdf file")
