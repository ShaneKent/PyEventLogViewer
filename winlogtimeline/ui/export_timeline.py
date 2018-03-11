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
        self.export_file_path = None
        # Export option config
        self.file_types = {
            '.csv <Comma-Separated Value>': '.csv',
            '.html <HypterText Markup Language>': '.html',
        }
        self.default_file_type = '.csv <Comma-Separated Value>'
        self.csv_delimiters = {
            'Comma': ',',
            'Space': ' ',
            'Tab': '\t',
        }
        self.default_csv_delimiter = 'Comma'
        self.exporters = {
            '.csv': self.export_csv,
            '.html': self.export_html,
        }

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

        # File path
        self.path_name = StringVar()
        self.path_name.set(os.path.abspath(self.current_project.get_path()))
        self.path_label = Label(self.work_container, text='File Path:')
        self.path_entry = Entry(self.work_container, textvariable=self.path_name)
        self.path_button = Button(self.work_container, width=3, text='...', command=self.callback_path_prompt)

        self.file_overwrite = Label(self.work_container, text='Warning:')

        # File Type
        self.type_label = Label(self.work_container, text='Type:')
        self.type_string = StringVar()
        self.type_string.set(self.default_file_type)
        self.type = OptionMenu(self.work_container, self.type_string, self.type_string.get(), *self.file_types.keys(),
                               command=self.display_settings)
        self.type.config(width='30')

        # CSV delimiters
        self.delimiter_label = Label(self.work_container, text='Delimiter:')
        self.delimiter_string = StringVar()
        self.delimiter_string.set(self.default_csv_delimiter)
        self.delimiter = OptionMenu(self.work_container, self.delimiter_string, self.delimiter_string.get(),
                                    *self.csv_delimiters.keys())

        # Column selectors
        self.columns_label = Label(self.work_container, text='Columns to Export:')
        self.columns_names = Record.get_headers()
        self.columns = []
        for c in self.columns_names:
            var = IntVar(value=1)
            self.columns.append([var, Checkbutton(self.work_container, text=c, variable=var)])

        # Filter options
        self.filters_var = BooleanVar(value=False)
        self.filters_checkbutton = Checkbutton(self.work_container, text="Use Current Filter?",
                                               variable=self.filters_var)

        # Buttons
        self.cancel_button = Button(self.work_container, text="Cancel", underline=0,
                                    command=self.callback_close_window)
        self.export_button = Button(self.work_container, text="Export", underline=0, command=self.export)
        self.bind("<Alt-c>", self.callback_close_window)
        self.bind("<Escape>", self.callback_close_window)
        self.bind("<Alt-e>", self.export)
        self.bind("<Return>", self.export)

        # Focus on window.
        self.focus_set()

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3
        i = 0

        # Export file name
        self.file_label.grid(row=i, column=0, columnspan=1, padx=padding, sticky='NES')
        self.file_entry.grid(row=i, column=1, columnspan=4, padx=padding, pady=padding, sticky='NESW')
        i += 1

        # Export path
        self.path_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.path_entry.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        self.path_button.grid(row=i, column=4, columnspan=1, padx=padding, pady=padding, sticky='NESW')
        i += 1

        # Warning block
        self.overwrite_row = i
        self.file_overwrite.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NEW')
        i += 1

        # Which file type to export as
        self.type_label.grid(row=i, column=0, padx=padding, sticky='NES')
        self.type.grid(row=i, column=1, columnspan=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        # Which CSV delimiter to use
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

        # Whether or not to apply the filter
        self.filters_checkbutton.grid(row=i, column=1, columnspan=1, padx=padding, sticky='NESW')
        self.cancel_button.grid(row=i, column=0, padx=padding, pady=padding, sticky='NESW')
        self.export_button.grid(row=i, column=2, padx=padding, pady=padding, sticky='NESW')
        i += 1

        # Containers
        self.work_container.columnconfigure(0, weight=4)
        self.work_container.grid(row=0, column=0, columnspan=5, rowspan=12, sticky='NW')

        self.container.columnconfigure(0, weight=4)
        self.container.pack(fill=BOTH)

        # Hide the warning block
        self.file_overwrite.grid_forget()
        # Disable the export button by default
        self.export_button.config(state=DISABLED)

    def callback_close_window(self, event=None):
        """
        Close the window.
        :return:
        """
        self.grab_release()
        self.destroy()

    def update_warning(self, full_file_name):
        """
        Updates the warning message based on the file name
        :param full_file_name: The file name (for display purposes)
        :return:
        """
        # Warn the user if attempting to overwrite an existing file
        if os.path.isfile(self.export_file_path):
            self.file_overwrite.grid(row=self.overwrite_row, column=0, columnspan=5, padx=3, pady=3, sticky='NESW')
            self.file_overwrite.config(
                text=(f"Warning: A file named '{full_file_name}' at the current location already exists.\n"
                      f"It may be overwritten."),
                foreground='red', anchor=CENTER)
        # Remove the warning
        else:
            self.file_overwrite.grid_forget()

    def update_file_path(self):
        """
        Updates the export file path based on user inputs.
        :return:
        """
        # Update the file path
        file_extension = self.file_types[self.type_string.get()]
        file_name = self.file_name.get()
        full_file_name = file_name + file_extension
        self.export_file_path = os.path.join(os.path.abspath(self.path_name.get()), full_file_name)
        # Update the warning message
        self.update_warning(full_file_name)

    def display_settings(self, *args):
        """
        Chooses what settings to display based on the choice made in the type dropdown.
        """
        padding = 3

        self.update_file_path()

        file_extension = self.file_types[self.type_string.get()]
        # Update the settings
        if file_extension == '.csv':
            self.delimiter_label.grid(row=self.delimiter_row, column=0, padx=padding, sticky='NES')
            self.delimiter.grid(row=self.delimiter_row, column=1, columnspan=1, padx=padding, pady=padding,
                                sticky='NESW')
        elif file_extension == '.html':
            self.delimiter_label.grid_forget()
            self.delimiter.grid_forget()
        # elif file_extension == '.pdf':
        #     self.delimiter_label.grid_forget()
        #     self.delimiter.grid_forget()

    def callback_path_prompt(self):
        """
        Callback used to kick off a directory selection prompt.
        :return:
        """
        workspace = filedialog.askdirectory()
        if len(workspace) > 0:
            self.path_name.set(os.path.abspath(workspace))

        self.update_file_path()

    def callback_update_path(self):
        """
        Callback used when either the workspace or title entry widgets are modified. Updates the value of the path entry
        widget.
        :return:
        """
        self.update_file_path()
        # Enable or disable the submit button
        if len(self.file_name.get()) > 0:
            self.export_button.config(state=NORMAL)
        else:
            self.export_button.config(state=DISABLED)

    def export(self, event=None):
        """
        Starts the export process.
        :return:
        """
        columns = {pair[1].cget('text'): pair[0].get() for pair in self.columns}
        file_name = self.file_name.get()

        # Guard against empty file names
        if file_name == '':
            messagebox.showerror('Error', 'Please provide a valid filename for the exported file.')
            return
        # Guard against the user specifying a file extension
        elif '.' in file_name:
            messagebox.showerror(
                'Error', (f"Please provide a valid filename without an extension.\nInstead of '{file_name}'"
                          f" you can use '{file_name.split('.')[0]}'"))
            return

        extension = self.file_types.get(self.type_string.get())
        # Gather the data to export
        if not self.filters_var.get():
            records = self.current_project.get_all_logs()
        else:
            records = self.master.master.get_filtered_records()
        records = sorted(records, key=lambda r: r.timestamp_utc)

        # Call the appropriate export function
        try:
            self.exporters[extension](columns, records)
        except Exception as e:
            messagebox.showerror('Error', f"Unable to export to '{self.export_file_path}'\nReason: {str(e)}")
            return

        # Provide feedback to the user
        self.master.master.update_status_bar(f'Successfully exported timeline to {self.export_file_path}')

        # Close the window
        self.callback_close_window()

    def export_csv(self, columns, records):
        """
        Exports the timeline as a CSV file.
        :return:
        """

        # Determine the CSV delimiter
        delimiter = self.csv_delimiters.get(self.delimiter_string.get())

        # Write to the file
        with open(self.export_file_path, 'w') as csv_file:
            w = writer(csv_file, delimiter=delimiter, quoting=0, lineterminator='\n')  # quoting == minimal quoting

            header = [key for key in columns if columns[key] == 1]
            w.writerow(header)

            booleans = [columns[key] for key in columns]

            for r in records:
                values = r.get_tuple()
                row = list(compress(values, booleans))

                w.writerow(row)

    def export_html(self, columns, records):
        """
        Exports the timeline as an html table.
        :return:
        """
        with open(self.export_file_path, 'w') as html_file:
            html_file.write('<html><body>\n')
            # Start the table
            html_file.write('<table style="width:100%">\n')
            # Write the headers
            header_row = '\n'.join(f'<th>{col}</th>' for col in columns)
            html_file.write(f'<tr>\n{header_row}\n</tr>\n')
            # Write the body
            highlights = self.current_project.config.get('events', {}).get('colors', {})
            for r in records:
                bg_color = highlights.get(r.event_source, {}).get(str(r.event_id), '#FFFFFF')
                row = '\n'.join(f'<td>{data}</td>' for data in r.get_tuple())
                html_file.write(f'<tr bgcolor="{bg_color}">\n{row}\n</tr>\n')
            html_file.write('</table>\n')
            html_file.write('</body></html>')
