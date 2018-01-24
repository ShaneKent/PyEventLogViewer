from tkinter import *
from tkinter import messagebox, filedialog
from tkinter import font
from tkinter.ttk import *
from threading import Thread
from winlogtimeline import util
from winlogtimeline import collector
from winlogtimeline.util.logs import Record
from .new_project import NewProject
from .tag_settings import TagSettings
from .import_window import ImportWindow
from .help_window import HelpWindow
from .export_timeline import ExportWindow
import os
import platform


def enable_disable_wrapper(_lambda):
    def decorate(f):
        def call(*args, **kwargs):
            if not _lambda(*args).enabled:
                _lambda(*args).update_status_bar('Notice: The selected action is disabled until a project is opened.')
                return None
            else:
                return f(*args, **kwargs)

        return call

    return decorate


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
        self.filter_section = Filters(self)
        self.timeline = None
        self.enabled = True
        self.system = platform.system()
        self.changes_made = False

        self.__disable__()
        self.protocol('WM_DELETE_WINDOW', self.__destroy__)

    def update_status_bar(self, text):
        """
        Updates the status bar.
        :param text: The message to place in the status bar.
        :return:
        """
        self.status_bar.update_status(text)

    def get_progress_bar_context_manager(self, max_value):
        """
        Returns a context manager which can be used to create and update the progress bar.
        :param max_value: The maximum value for the progress bar.
        :return:
        """
        return StatusBarContextManager(self.status_bar, max_value)

    def create_project(self):
        window = NewProject(self)
        window.grab_set()

    def open_color_settings(self):
        window = TagSettings(self)
        window.grab_set()

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
        self.winfo_toplevel().title(f'PyEventLogViewer - {self.current_project.get_path().split(os.path.sep)[-1]}')
        self.create_new_timeline()
        self.__enable__()

    def close_project(self):
        """
        Prompts the user to save the project and then closes it.
        :return:
        """
        if self.current_project is not None and self.changes_made:
            answer = messagebox.askquestion(title='Save Before Close',
                                            message='Would you like to save the currently opened project before '
                                                    'closing it?', type=messagebox.YESNOCANCEL)

            if answer == messagebox.YES:
                self.changes_made = False
                self.current_project.close()
                self.current_project = None
            elif answer == messagebox.NO:
                self.current_project = None
            else:
                return

        if self.timeline is not None:
            self.timeline.pack_forget()
            self.timeline = None

    @enable_disable_wrapper(lambda *args: args[0])
    def import_function(self, file_name, alias):
        """
        Function used to kick off the log import process.
        :param file_name: The path to the file to import.
        :param alias: A unique alias for the file.
        :return:
        """
        def callback():
            # Prepare status bar callback.
            text = '{file}: {status}'.format(file=os.path.basename(file_name), status='{status}')

            # Start the import log process.
            collector.import_log(file_name, alias, self.current_project, '',
                                 lambda s: self.update_status_bar(text.format(status=s)),
                                 self.get_progress_bar_context_manager)

            # Create or update the timeline.
            self.create_new_timeline()
            self.changes_made = True

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
            if h is None:
                h = Record.get_headers()
            r = [record.get_tuple() for record in r]

            # Delete the old timeline if it exists
            if self.timeline is not None:
                self.timeline.pack_forget()

            self.update_status_bar('Rendering timeline...')
            # Create the new timeline
            self.timeline = Timeline(self, h, r)

            self.update_status_bar('')
            # Enable all timeline interaction buttons
            self.__enable__()

        t = Thread(target=callback)
        t.start()

    def __disable__(self):
        self.enabled = False
        if self.system != 'Darwin':
            self.toolbar.__disable__()
            #self.query_bar.__disable__()
            # self.filter_section.__disable__()
            self.menu_bar.__disable__()

    def __enable__(self):
        self.enabled = True
        if self.system != 'Darwin':
            self.toolbar.__enable__()
            # self.query_bar.__enable__()
            # self.filter_section.__enable__()
            self.menu_bar.__enable__()

    def __destroy__(self):
        self.close_project()
        self.destroy()


class Timeline(Frame):
    def __init__(self, parent, headers, data, **kwargs):
        super().__init__(parent, **kwargs)

        # Class variables
        self.headers = headers
        self.col_width = {header: font.Font().measure(header) for header in headers}

        # Create and place the widgets
        self._init_widgets()
        self.setup_columns()
        self.update_column_widths(data)
        self.update_tags(parent.current_project.config['events'])
        self.populate_timeline(data)
        self.sort_column('Timestamp (UTC)', False)
        self._place_widgets()

    def _init_widgets(self):
        # Treeview
        self.tree = Treeview(columns=self.headers, show='headings')
        # Scrollbars
        self.vsb = Scrollbar(orient='vertical', command=self.tree.yview)
        self.hsb = Scrollbar(orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=self.vsb.set, xscrollcommand=self.hsb.set)

    def _place_widgets(self):
        # Tree
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self)
        # Scrollbars
        self.vsb.grid(column=1, row=0, sticky='ns', in_=self)
        self.hsb.grid(column=0, row=1, sticky='ew', in_=self)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.pack(fill='both', expand=True)

    def update_tags(self, tags):
        """
        Updates the colors associated with record tags.
        :param tags: The tags to update.
        :return:
        """
        for tag, color in tags.items():
            self.tree.tag_configure(tag, background=color)

    def setup_columns(self):
        """
        Inserts headers into the timeline.
        :return:
        """
        # Set up the columns
        for col in self.headers:
            self.tree.heading(col, text=col.title(), command=lambda _col=col: self.sort_column(_col, False))

    def populate_timeline(self, data):
        """
        Populates the timeline.
        :param data: The data to insert into the timeline.
        :return:
        """
        # Insert the data
        self.master.update_status_bar('Populating timeline...')
        with self.master.get_progress_bar_context_manager(len(data)) as progress_bar:
            for i, row in enumerate(data):
                # TODO: Change the tags to use event source and event id instead of just event id
                self.tree.insert('', 'end', values=row, tags=str(row[1]))
                if not i % 100:
                    progress_bar.update_progress(100)
        self.master.update_status_bar('Finished populating timeline.')

    def update_column_widths(self, data):
        """
        Calculates the widths for the columns.
        :param data: The data to iterate over.
        :return:
        """
        known_s_widths = dict()
        known_widths = dict()
        excluded_headers = {'Details', }
        measurement_font = font.Font()

        # Determine the column widths
        self.master.update_status_bar("Calculating the column widths...")
        with self.master.get_progress_bar_context_manager(len(data)) as progress_bar:
            for j, row in enumerate(data):
                # Update the column widths
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
                    if width > self.col_width[self.headers[i]]:
                        self.col_width[self.headers[i]] = width

                # Update the progress bar
                if not j % 100:
                    progress_bar.update_progress(100)

        self.master.update_status_bar('Finished calculating column widths.')

        # Updating the column widths
        for col in self.headers:
            self.tree.column(col, width=self.col_width[col])

    def sort_column(self, col, reverse):
        """
        Sorts the timeline based on a particular column.
        :param col: The column to sort.
        :param reverse: Whether or not to sort in reverse order.
        :return:
        """
        column_elements = [(self.tree.set(k, col), k) for k in self.tree.get_children('')]
        column_elements.sort(reverse=reverse)

        for index, (val, k) in enumerate(column_elements):
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

        #self.button = Button(self, text="Query", command=lambda: collector.collect.filter_logs(None, self.master.current_project, None))
        #self.button.pack(side=LEFT)
        # --

    def __disable__(self):
        self.button.config(state=DISABLED)
        self.drop_down.config(state=DISABLED)

    def __enable__(self):
        self.button.config(state=NORMAL)
        self.drop_down.config(state=NORMAL)


class StatusBar(Frame):
    def __init__(self, parent):
        super().__init__(parent, relief=SUNKEN)

        self.progress = None
        self._init_widgets()
        self._place_widgets()

    def _init_widgets(self):
        self.status = Label(self, text='Notice: Create a new project or open an existing project to get started.',
                            anchor=W)

    def _place_widgets(self):
        padding = 2
        self.status.grid(row=0, column=0, padx=padding, pady=padding, sticky='W')
        # self.progress.grid(row=0, column=1, padx=padding, pady=padding, sticky='E')
        self.columnconfigure(0, weight=4)
        self.pack(side=BOTTOM, fill=X)

    def update_status(self, message):
        """
        Updates the message displayed on the status bar.
        :param message: The message to display.
        :return:
        """
        self.status.config(text=message)


class StatusBarContextManager:
    def __init__(self, parent, max_value):
        self.parent = parent
        self.max_value = max_value

    def __enter__(self):
        self.parent.progress = Progressbar(self.parent, length=200, maximum=self.max_value, mode='determinate')
        self.parent.progress.grid(row=0, column=1, padx=2, pady=2, sticky='E')
        return self

    def __exit__(self, *args):
        self.parent.progress.grid_forget()

    def update_progress(self, steps):
        """
        Increments the progress bar.
        :param steps: The number of steps to increment the progress bar by.
        :return:
        """
        self.parent.progress.step(steps)


class Toolbar(Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, borderwidth=1, relief=SUNKEN, **kwargs)

        self.import_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'import.gif'))
        self.export_photo = PhotoImage(file=util.data.get_package_data_path(__file__, 'icons', 'export.gif'))

        self.import_button = Button(self, image=self.import_photo, width='20',
                                    command=self.master.menu_bar.import_button_function)
        self.export_button = Button(self, image=self.export_photo, width='20',
                                    command=self.master.menu_bar.export_button_function)

        self.import_button.pack()
        self.export_button.pack()

        self.pack(side=LEFT, fill=Y)

    def __disable__(self):
        self.import_button.config(state=DISABLED)
        self.export_button.config(state=DISABLED)

    def __enable__(self):
        self.import_button.config(state=NORMAL)
        self.export_button.config(state=NORMAL)


class MenuBar(Menu):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        parent.config(menu=self)

        # File
        self.file_menu = Menu(self, **kwargs)
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

        # File -> Export
        self.file_menu.add_command(label="Export Timeline", command=self.export_button_function, underline=0,
                                   accelerator='Ctrl+E')
        parent.bind('<Control-e>', self.export_button_function)

        # Tools
        self.tool_menu = Menu(self, **kwargs)
        self.add_cascade(label='Tools', menu=self.tool_menu, underline=0)
        # Tools -> Timeline Colors
        self.tool_menu.add_command(label='Timeline Colors', command=self.color_settings_function, underline=0)
        # Tools -> Import Log
        self.tool_menu.add_command(label='Import Log File', command=self.import_button_function, underline=0,
                                   accelerator='Ctrl+I')
        parent.bind('<Control-i>', self.import_button_function)

        # Help
        self.help_menu = Menu(self, **kwargs)
        self.add_cascade(label='Help', menu=self.help_menu, underline=0)
        # Help -> About
        self.help_menu.add_command(label='About', command=self.about_function, underline=0)
        # Help -> License
        self.help_menu.add_command(label='License', command=self.license_function, underline=0)
        # Help -> Contact
        self.help_menu.add_command(label='Contact', command=self.contact_function, underline=0)


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
        projects_path = os.path.join(util.data.get_appdir(), 'Projects')
        filename = filedialog.askopenfilename(initialdir=projects_path, title='Open a Project File',
                                              filetypes=(('ELV Project File', '*.elv'),))
        if len(filename) > 0:
            self.master.close_project()
            self.master.open_project(filename)
            if self.master.current_project is not None:
                self.master.update_status_bar('Project opened at ' + self.master.current_project.get_path())
            else:
                self.master.update_status_bar('Failed to open the project at ' + filename)
        self.master.changes_made = False

    @enable_disable_wrapper(lambda *args: args[0].master)
    def save_project_function(self, event=None):
        """
        Callback function for File -> Save. Saves the current project.
        :param event: A click or key press event.
        :return:
        """
        self.master.current_project.save()
        self.master.update_status_bar('Project saved')
        self.master.changes_made = False

    @enable_disable_wrapper(lambda *args: args[0].master)
    def color_settings_function(self, event=None):
        """
        Callback function for Tools -> Timeline Colors. Alters the colors for the current project.
        :param event: A click or key press event.
        :return:
        """
        self.master.open_color_settings()

    @enable_disable_wrapper(lambda *args: args[0].master)
    def import_button_function(self, event=None):
        """
        Callback function for Tools -> Import Log File. Launches the log file import window.
        :return:
        """
        wizard = ImportWindow(self)
        wizard.grab_set()

    @enable_disable_wrapper(lambda *args: args[0].master)
    def export_button_function(self, event=None):
        """
        TODO: Determine whether or not this function and associated button are necessary.
        :param event:
        :return:
        """
        wizard = ExportWindow(self, self.master.current_project)
        wizard.grab_set()

    def about_function(self, event=None):
        """
        :param event:
        :return:
        """
        wizard = HelpWindow(self, "about")
        wizard.grab_set()

    def license_function(self, event=None):
        """
        :param event:
        :return:
        """
        wizard = HelpWindow(self, "license")
        wizard.grab_set()

    def contact_function(self, event=None):
        """
        :param event:
        :return:
        """
        wizard = HelpWindow(self, "contact")
        wizard.grab_set()

    def __enable__(self):
        self.entryconfig('Tools', state=NORMAL)
        self.file_menu.entryconfig('Save', state=NORMAL)
        self.file_menu.entryconfig('Export Timeline', state=NORMAL)

    def __disable__(self):
        self.entryconfig('Tools', state=DISABLED)
        self.file_menu.entryconfig('Save', state=DISABLED)
        self.file_menu.entryconfig('Export Timeline', state=DISABLED)


class Filters(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.pack(side=TOP, fill=X)

        # Filter Label
        self.flabel = Label(self, text='Filters:', anchor=W, **kwargs)
        self.flabel.pack(side=LEFT)

        # List of filter columns
        self.colList = ['- Select Column -']
        self.create_colList(self.colList)

        # Column variable
        self.cvar = StringVar(self)
        self.cvar.set(self.colList[0])

        # Filter columns drop down menu
        self.columns = OptionMenu(self, self.cvar, *self.colList)
        self.columns.config(width='15')
        self.columns.pack(side=LEFT)

        # List of operation columns
        self.opList = ['- Select Operation -']

        # Operation variable
        self.ovar = StringVar(self)
        self.ovar.set(self.opList[0])

        # Filter operations drop down menu
        self.operations = OptionMenu(self, self.ovar, *self.opList)
        self.operations.config(width='15')
        self.operations.pack(side=LEFT)

        #User entered filter value variable
        self.val = StringVar(self)

        #Filter operation value entry field
        self.filterVal = Entry(self, textvariable=self.val)
        self.filterVal.config(width='15')
        self.filterVal.pack(side=LEFT)

        #self.button = Button(self, text="Query", command=lambda: collector.filter.filter_logs(self.master.current_project, self.filter_config()))
        self.button = Button(self, text="Query", command=lambda: self.apply_filter())
        self.button.pack(side=LEFT)

        self.cvar.trace_add('write', lambda *args: self.create_opList())

    def __disable__(self):
        self.flabel.config(state=DISABLED)
        self.columns.config(state=DISABLED)

    def __enable__(self):
        self.flabel.config(state=NORMAL)
        self.columns.config(state=NORMAL)

    def get_opList(self):
        return self.opList

    def create_colList(self, colList):
        tmp = Record.get_headers()
        for col in tmp:
            colList.append(col)

    def create_opList(self):
        inttype = {'Event ID', 'Record Number', 'Recovered'}
        strtype = {'Description', 'Details', 'Event Source', 'Event Log', 'Account', 'Computer Name'}

        column = self.cvar.get()
        print(column)

        self.opList = ['- Select Operation -']
        if column in inttype:
            print('Value is int')
            self.opList = ['=', '<', '>']
        elif column in strtype:
            print('Value is str')
            self.opList = ['Is', 'Contains']


        self.operations['menu'].delete(0, 'end')
        for choice in self.opList:
            self.operations['menu'].add_command(label=choice, command=lambda c=choice: self.ovar.set(c))
        self.ovar.set(self.opList[0])

    def apply_filter(self):
        config = self.filter_config()
        logs = collector.filter_logs(self.master.current_project, config)

        self.master.create_new_timeline(records=logs)

    def filter_config(self):
        col = self.cvar.get()
        if col == 'Event ID':
            col = 'event_id'
        config = (col, self.ovar.get(), self.filterVal.get())

        print(config)
        return [config]
