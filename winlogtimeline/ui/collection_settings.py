from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import re

import itertools

from winlogtimeline.collector.parser import parsers


class CollectionSettings(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables
        self.tags = dict()
        self.changes_made = False

        # Window Parameters
        self.title('Custom Record Collection')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        # Scrape the builtin records from the parser
        self.builtin_events = [(source, event)
                               for source, events in parsers.items()
                               for event in events.keys()]
        custom_events = parent.current_project.config.get('events', {}).get('custom', {})
        self.user_events = [(source, event)
                            for source, events in custom_events.items()
                            for event in events]
        self.populate_events()
        self._place_widgets()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Master container frame
        self.container = Frame(self)
        # Treeview for records
        self.listbox_container = Frame(self.container)
        self.event_list = Treeview(self.listbox_container, columns=('source', 'id'), show='headings')
        # Set up the tree headings
        self.event_list.heading('source', text='Event Source', command=lambda: self.sort_column('source', False))
        self.event_list.heading('id', text='Event ID', command=lambda: self.sort_column('id', False))
        # Set up the tree columns
        self.event_list.column('id', minwidth=0, width=60, stretch=NO)
        self.event_list.column('source', minwidth=0, width=100, stretch=YES)
        # Set up the scrollbars
        self.vsb = Scrollbar(self.listbox_container, orient='vertical', command=self.event_list.yview)
        self.hsb = Scrollbar(self.listbox_container, orient='horizontal', command=self.event_list.xview)
        self.event_list.configure(yscrollcommand=self.vsb.set)
        self.event_list.configure(xscrollcommand=self.hsb.set)
        # Buttons for editing records
        self.add_button = Button(self.container, text='Add', command=self.callback_add_event, underline=0)
        self.bind('<Alt-a>', self.callback_add_event)
        self.delete_button = Button(self.container, text='Delete', command=self.callback_remove_event, underline=0)
        self.bind('<Alt-d>', self.callback_remove_event)
        # Finish and cancel buttons
        self.finish_button = Button(self.container, text='Finish', command=self.callback_finish, underline=0)
        self.cancel_button = Button(self.container, text='Cancel', command=self.callback_cancel, underline=0)
        self.bind('<Alt-f>', self.callback_finish)
        self.bind('<Return>', self.callback_finish)
        self.bind('<Alt-c>', self.callback_cancel)
        self.bind('<Escape>', self.callback_cancel)

        # Focus on window.
        self.focus_set()

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3
        # Listbox for tags
        self.event_list.grid(row=0, column=0, columnspan=4, sticky='NESW')
        self.vsb.grid(row=0, column=4, sticky='NESW')
        self.hsb.grid(row=1, column=0, sticky='NESW')
        self.listbox_container.columnconfigure(0, weight=4)
        self.listbox_container.grid(row=0, column=0, columnspan=5, padx=padding, pady=padding, sticky='NESW')
        # Buttons for editing tags
        self.add_button.grid(row=5, column=1, padx=padding, pady=padding, sticky='E')
        self.delete_button.grid(row=5, column=2, padx=padding, pady=padding, sticky='EW')
        # Finish and cancel buttons
        self.finish_button.grid(row=5, column=3, padx=padding, pady=padding, sticky='EW')
        self.cancel_button.grid(row=5, column=4, padx=padding, pady=padding, sticky='EW')
        # Master container frame
        self.container.columnconfigure(1, minsize=100)
        self.container.pack(side=LEFT, fill=BOTH)

    def sort_column(self, col, reverse):
        """
        Sorts the tag list based on a particular column.
        :param col: The column to sort.
        :param reverse: Whether or not to sort in reverse order.
        :return:
        """
        column_elements = [(self.event_list.set(k, col), k) for k in self.event_list.get_children('')]
        if col == 'id':
            column_elements = [(int(v), k) for v, k in column_elements]
        column_elements.sort(reverse=reverse)

        for index, (val, k) in enumerate(column_elements):
            self.event_list.move(k, '', index)

        self.event_list.heading(col, command=lambda _col=col: self.sort_column(_col, not reverse))

    def populate_events(self):
        """
        Iterates over the builtin and user-specified events to build the event list
        :return:
        """
        for source, event in self.builtin_events:
            self.event_list.insert('', 'end', values=(source, int(event)), tags=('builtin',))
        for source, event in self.user_events:
            self.event_list.insert('', 'end', values=(source, int(event)))
        self.event_list.tag_configure('builtin', background='#DDDDDD')

    def insert_event(self, source, event):
        """
        Inserts an event into the event list.
        :param source: The event source.
        :param event: The event id.
        :return:
        """
        self.event_list.insert('', 'end', values=(source, int(event)))
        self.user_events.append((source, event))

    def callback_add_event(self, event=None):
        """
        Creates a dialog window for the user to enter a new event.
        :return:
        """
        window = EventPrompt(self)
        window.grab_set()

    def callback_remove_event(self, event=None):
        """
        Removes an event as long as it isn't a builtin.
        :return:
        """
        selection = self.event_list.focus()
        if not selection:
            return
        item = self.event_list.item(selection)
        if 'builtin' in item['tags']:
            messagebox.showerror('Error', 'Cannot remove builtin event type')
            return
        source, event = item['values']
        self.user_events.remove((source, str(event)))
        self.event_list.delete(selection)
        self.changes_made = True

    def callback_finish(self, event=None):
        """
        Callback used to finish making changes to the tags and return to master.
        :return:
        """
        custom_events = dict()
        for source, elems in itertools.groupby(sorted(self.user_events), lambda e: e[0]):
            custom_events[source] = [e[1] for e in elems]
        self.master.current_project.config['events']['custom'] = custom_events
        self.master.changes_made |= self.changes_made
        self.destroy()

    def callback_cancel(self, event=None):
        """
        Callback used to discard changes made. Destroys the widget and returns control to the master
        without making any changes.
        :return:
        """
        self.destroy()

    def __destroy__(self):
        """
        Returns focus and control to the master.
        :return:
        """
        self.grab_release()


class EventPrompt(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Window settings
        self.title('New Tag')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self._place_widgets()

    def _init_widgets(self):
        self.container = Frame(self)
        self.source_label = Label(self.container, text='Event Source')
        self.source_entry = Entry(self.container)
        self.id_label = Label(self.container, text='Event ID')
        id_vcmd = (self.container.register(self.validate_command_id), '%d', '%P')
        self.id_entry = Entry(self.container, validate='key', validatecommand=id_vcmd)
        self.ok_button = Button(self.container, text='Ok', command=self.callback_ok)

    def _place_widgets(self):
        padding = 3
        self.source_label.grid(row=0, column=0, columnspan=3, padx=padding, pady=padding, sticky='EW')
        self.source_entry.grid(row=1, column=0, columnspan=3, padx=padding, pady=padding, sticky='EW')
        self.id_label.grid(row=2, column=0, columnspan=3, padx=padding, pady=padding, sticky='EW')
        self.id_entry.grid(row=3, column=0, columnspan=3, padx=padding, pady=padding, sticky='EW')
        self.ok_button.grid(row=4, column=1, padx=padding, sticky='NESW')
        self.container.pack()

    @staticmethod
    def validate_command_id(action, value):
        """
        Restricts entry to only allow integers.
        :return:
        """
        if action != '1':
            return True
        if re.match(r'^[0-9]+$', value):
            return True
        return False

    def callback_ok(self):
        source, event = self.source_entry.get(), str(self.id_entry.get())
        if not all((source, event)):
            messagebox.showerror('Error', 'You must enter a value.')
            return
        if (source, event) in self.master.user_events or (source, event) in self.master.builtin_events:
            messagebox.showerror('Error', 'That tag already exists.')
            return
        self.master.insert_event(source, event)
        self.master.changes_made = True
        self.destroy()

    def __destroy__(self):
        """
        Returns focus and control to the master.
        :return:
        """
        self.grab_release()
