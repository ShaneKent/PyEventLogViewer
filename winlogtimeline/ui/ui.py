from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import font
from tkinter.ttk import *

from threading import Thread
from winlogtimeline import util
from winlogtimeline import collector

from .new_project_wizard import NewProjectWizard
from .import_wizard import ImportWizard

import os


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.winfo_toplevel().title('PyEventLogViewer')
        self.minsize(width=800, height=600)

        self.program_config = util.data.open_config()
        self.current_project = None

        self.menu_bar = MenuBar(self, tearoff=False)
        self.status_bar = StatusBar(self)
        self.toolbar = Toolbar(self)
        self.query_bar = QueryBar(self)
        self.event_section = None

        self.__disable__()
        self.protocol('WM_DELETE_WINDOW', self.__destroy__)

    def update_status_bar(self, text):
        self.status_bar.status.config(text=text)

    def create_project(self):
        wizard = NewProjectWizard(self)
        wizard.grab_set()

    def open_project(self, project_path):
        """
        Opens a project. This will create it if it doesn't already exist.
        :param project_path: The path to the project elv file.
        :return:
        """
        self.current_project = util.project.Project(project_path)
        # Check that the project was able to be created
        if self.current_project.exception is not None:
            self.current_project = None
            return
        self.create_new_timeline()
        self.__enable__()

    def close_project(self):
        """
        Prompts the user to save the project and then closes it.
        :return:
        """
        if self.current_project is not None:
            answer = messagebox.askquestion(title='Save Before Close',
                                            message='Would you like to save the currently opened project before '
                                                    'closing it?', type=messagebox.YESNOCANCEL)

            if answer == messagebox.YES:
                self.current_project.close()
                self.current_project = None
            elif answer == messagebox.NO:
                self.current_project = None
            else:
                return

        if self.event_section is not None:
            self.event_section.pack_forget()
            self.event_section = None

    def import_function(self, file_name, alias):

        def callback():
            # Prepare status bar callback.
            text = '{file}: {status}'.format(file=os.path.basename(file_name), status='{status}')

            # Start the import log process.
            collector.import_log(file_name, alias, self.current_project, '',
                                 lambda s: self.update_status_bar(text.format(status=s)))

            # Create or update the timeline.
            self.create_new_timeline()

        t = Thread(target=callback)
        t.start()

        return

    def create_new_timeline(self, headers=None, records=None):
        """
        Function for creating/updating the event section.
        :param headers: A tuple containing the column titles. These should be in the same order as the values in
        records.
        :param records: A list of tuples containing the record values.
        :return:
        """

        def callback(h=headers, r=records):
            # Disable all timeline interaction buttons to prevent a timeline duplication bug
            self.__disable__()
            self.update_status_bar('Loading records...')

            # Get all records if they weren't provided
            if r is None:
                r = self.current_project.get_all_logs()
                if len(r) == 0:
                    self.__enable__()
                    self.update_status_bar('Done.')
                    return
                h = r[0].get_headers()
                r = [record.get_tuple() for record in r]

            # Delete the old timeline if it exists
            if self.event_section is not None:
                self.event_section.pack_forget()

            self.update_status_bar('Rendering timeline...')
            # Create the new timeline
            self.event_section = EventSection(self, h, r)

            self.update_status_bar('')
            # Enable all timeline interaction buttons
            self.__enable__()

        t = Thread(target=callback)
        t.start()

    def __disable__(self):
        self.toolbar.__disable__()
        self.query_bar.__disable__()

    def __enable__(self):
        self.toolbar.__enable__()
        self.query_bar.__enable__()

    def __destroy__(self):
        self.close_project()
        self.destroy()


class EventSection(Frame):
    def __init__(self, parent, headers, data, **kwargs):
        # Set up the frame
        super().__init__(parent, **kwargs)
        self.headers = headers
        self.pack(fill='both', expand=True)
        # Treeview
        self.tree = Treeview(columns=self.headers, show='headings')

        col_width = {header: font.Font().measure(header) for header in headers}
        # TODO see if this can be done in a reasonable amount of time

        # Dynamic programming?
        known_s_widths = dict()
        known_widths = dict()
        excluded_headers = {'Details',}
        measurement_font = font.Font()

        # Determine the column widths
        self.master.update_status_bar("Determining the column widths.")
        j = 1
        for row in data:

            if j % 10 == 0:
                self.master.update_status_bar('Prepared information for {} records.'.format(j))
            j += 1

            for i, v in enumerate(row):
                if self.headers[i] in excluded_headers:
                    continue
                if type(v) is str:
                    if len(v) not in known_s_widths:
                        known_s_widths[len(v)] = measurement_font.measure(v)
                    width = known_s_widths[len(v)]
                else:
                    if v not in known_widths:
                        known_widths[v] = measurement_font.measure(v)
                    width = known_widths[v]
                if width > col_width[self.headers[i]]:
                    col_width[self.headers[i]] = width

        # Set up the columns
        for col in self.headers:
            self.tree.heading(col, text=col.title(), command=lambda _col=col: self.sort_column(_col, False))
            self.tree.column(col, width=col_width[col])

        # Load the tags from the config
        for event in self.master.program_config['events']:
            self.tree.tag_configure(event['event_id'], background=event['color'])

        # Insert the data
        i = 1
        for row in data:
            if i % 10 == 0:
                self.master.update_status_bar('{} records ready to render.'.format(i))
            i += 1

            # TODO: Change the tags to use event source and event id instead of just event id
            self.tree.insert('', 'end', values=row, tags=str(row[1]))

        # Scrollbars
        vsb = Scrollbar(orient='vertical', command=self.tree.yview)
        hsb = Scrollbar(orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self)
        vsb.grid(column=1, row=0, sticky='ns', in_=self)
        hsb.grid(column=0, row=1, sticky='ew', in_=self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def sort_column(self, col, reverse):
        l = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        l.sort(reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tree.move(k, '', index)

        self.tree.heading(col, command=lambda _col=col: self.sort_column(_col, not reverse))


class QueryBar(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=X)

        self.label = Label(self, text='Show Events:', anchor=W, **kwargs)
        self.label.pack(side=LEFT)

        self.variable = StringVar(self)
        self.variable.set('All')

        self.drop_down = OptionMenu(self, self.variable, 'System Startup', 'System Shutdown', 'Time Change',
                                    'All')
        self.drop_down.config(width='15')
        self.drop_down.pack(side=LEFT)

        # -- REMOVE WHEN NOT NEEDED. Only for prototyping reasons.

        self.button = Button(self, text="Query", command=lambda: collector.filter_logs(None, None, None))
        self.button.pack(side=LEFT)
        # --

    def __disable__(self):
        self.button.config(state=DISABLED)
        self.drop_down.config(state=DISABLED)

    def __enable__(self):
        self.button.config(state=NORMAL)
        self.drop_down.config(state=NORMAL)


class StatusBar(Label):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent)
        self.status = Label(parent, text='Notice: Create a new project or open an existing project to get started.',
                            borderwidth=1, relief=SUNKEN, anchor=W, *args,
                            **kwargs)
        self.status.pack(side=BOTTOM, fill=X)


class Toolbar(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, borderwidth=1, relief=SUNKEN, **kwargs)

        self.import_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'import.gif'))
        self.format_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'format.gif'))

        self.import_button = Button(self, image=self.import_photo, width='20',
                                    command=lambda: self.import_button_function())
        self.format_button = Button(self, image=self.format_photo, width='20',
                                    command=lambda: self.format_button_function())

        self.import_button.pack()
        self.format_button.pack()

        self.pack(side=LEFT, fill=Y)

    def __disable__(self):
        self.import_button.config(state=DISABLED)
        self.format_button.config(state=DISABLED)

    def __enable__(self):
        self.import_button.config(state=NORMAL)
        self.format_button.config(state=NORMAL)

    def import_button_function(self):
        wizard = ImportWizard(self)
        wizard.grab_set()

    def format_button_function(self):
        self.master.status_bar.status.config(text='"Format" button pressed.')
        return


class MenuBar(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        parent.config(menu=self)

        self.file_menu = Menu(self, **kwargs)

        # File
        self.add_cascade(label='File', menu=self.file_menu, underline=0)

        # File -> New Project (Ctrl+N)
        self.file_menu.add_command(label='New', command=self.new_project_function, underline=0,
                                   accelerator='Ctrl+N')
        parent.bind('<Control-n>', self.new_project_function)

        # File -> Open... (Ctrl+O)
        self.file_menu.add_command(label='Open...', command=self.open_project_function, underline=0,
                                   accelerator='Ctrl+O')
        parent.bind('<Control-o>', self.open_project_function)

        # File -> Save
        self.file_menu.add_command(label='Save', command=self.save_project_function, underline=0,
                                   accelerator='Ctrl+S')
        parent.bind('<Control-s>', self.save_project_function)

    def new_project_function(self, event=None):
        """
        Callback function for File -> New. Closes the current project and kicks of the project creation wizard.
        :param event: A click or key press event.
        :return:
        """
        self.master.close_project()
        self.master.create_project()
        if self.master.current_project is not None:
            self.master.update_status_bar('Project created at ' + self.master.current_project.get_path())
        else:
            self.master.update_status_bar('Project creation failed')

    def open_project_function(self, event=None):
        """
        Callback function for File -> Open. Closes the current project and kicks off the open project UI.
        :param event: A click or key press event.
        :return:
        """
        self.master.close_project()
        projects_path = os.path.join(util.data.get_appdir(), 'Projects')
        filename = filedialog.askopenfilename(initialdir=projects_path, title='Open a Project File',
                                              filetypes=(('ELV Project File', '*.elv'),))
        if len(filename) > 0:
            self.master.open_project(filename)
            if self.master.current_project is not None:
                self.master.update_status_bar('Project opened at ' + self.master.current_project.get_path())
            else:
                self.master.update_status_bar('Failed to open the project at ' + filename)

    def save_project_function(self, event=None):
        """
        Callback function for File -> Save. Saves the current project.
        :param event: A click or key press event.
        :return:
        """
        self.master.current_project.save()
        self.master.update_status_bar('Project saved!')
