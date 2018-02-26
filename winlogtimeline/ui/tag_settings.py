from tkinter import *
from tkinter import messagebox
from tkinter.ttk import *
import re


class TagSettings(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables
        self.tags = dict()
        self.changes_made = False

        # Window Parameters
        self.title('Record Highlight Settings')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self.populate_tags(parent.current_project.config.get('events', {}).get('colors', {}))
        self._place_widgets()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Master container frame
        self.container = Frame(self)
        # Treeview for tags
        self.listbox_container = Frame(self.container)
        self.tag_list = Treeview(self.listbox_container, columns=('source', 'id'), show='headings')
        # Set up the tree headings
        self.tag_list.heading('source', text='Event Source', command=lambda: self.sort_column('source', False))
        self.tag_list.heading('id', text='Event ID', command=lambda: self.sort_column('id', False))
        # Set up the tree columns
        self.tag_list.column('id', minwidth=0, width=60, stretch=NO)
        self.tag_list.column('source', minwidth=0, width=100, stretch=YES)
        self.tag_list.bind('<<TreeviewSelect>>', self.callback_update_select_background)
        # Scrollbar settings
        self.vsb = Scrollbar(self.listbox_container, orient='vertical', command=self.tag_list.yview)
        self.hsb = Scrollbar(self.listbox_container, orient='horizontal', command=self.tag_list.xview)
        self.tag_list.configure(yscrollcommand=self.vsb.set)
        self.tag_list.configure(xscrollcommand=self.hsb.set)
        # Color preview
        self.color_block = Canvas(self.container, width=300, height=20, relief=SUNKEN)
        self.color_block_rect = self.color_block.create_rectangle(0, 0, 301, 21, fill='#FFFFFF')
        self.color_block_text = self.color_block.create_text(5, 5, anchor='nw',
                                                             text='The quick brown fox jumps over the lazy dog.')
        # Sliders
        self.slider_container = Frame(self.container)
        # Red config
        self.red = IntVar()
        self.r_label = Label(self.slider_container, text='R: ')
        self.r_slider = Scale(self.slider_container, from_=0, to=255, variable=self.red,
                              command=lambda *args: self.truncate(self.r_slider))
        self.r_value_label = Label(self.slider_container, text='0')
        self.red.trace('w', lambda *args: self.callback_update_label(self.red, self.r_value_label))
        self.r_slider.set(255)
        # Green config
        self.green = IntVar()
        self.g_label = Label(self.slider_container, text='G: ')
        self.g_slider = Scale(self.slider_container, from_=0, to=255, variable=self.green,
                              command=lambda *args: self.truncate(self.g_slider))
        self.g_value_label = Label(self.slider_container, text='0')
        self.green.trace('w', lambda *args: self.callback_update_label(self.green, self.g_value_label))
        self.g_slider.set(255)
        # Blue config
        self.blue = IntVar()
        self.b_label = Label(self.slider_container, text='B: ')
        self.b_slider = Scale(self.slider_container, from_=0, to=255, variable=self.blue,
                              command=lambda *args: self.truncate(self.b_slider))
        self.b_value_label = Label(self.slider_container, text='0')
        self.blue.trace('w', lambda *args: self.callback_update_label(self.blue, self.b_value_label))
        self.b_slider.set(255)
        # Buttons for editing tags
        self.add_button = Button(self.container, text='Add', command=self.callback_add_tag, underline=0)
        self.bind('<Alt-a>', self.callback_add_tag)
        self.delete_button = Button(self.container, text='Delete', command=self.callback_remove_tag, underline=0)
        self.bind('<Alt-d>', self.callback_remove_tag)
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
        self.tag_list.grid(row=0, column=0, columnspan=4, sticky='NESW')
        self.vsb.grid(row=0, column=4, sticky='NESW')
        self.hsb.grid(row=1, column=0, sticky='NESW')
        self.listbox_container.columnconfigure(0, weight=4)
        self.listbox_container.grid(row=0, column=0, columnspan=5, padx=padding, pady=padding, sticky='NESW')
        # Color box
        self.color_block.grid(row=1, column=0, columnspan=5, padx=padding, pady=padding, sticky='NS')
        # Red config
        self.r_label.grid(row=2, column=0, sticky='EW')
        self.r_slider.grid(row=2, column=1, columnspan=3, sticky='EW')
        self.r_value_label.grid(row=2, column=4, sticky='EW')
        # Green config
        self.g_label.grid(row=3, column=0, sticky='EW')
        self.g_slider.grid(row=3, column=1, columnspan=3, sticky='EW')
        self.g_value_label.grid(row=3, column=4, sticky='EW')
        # Blue config
        self.b_label.grid(row=4, column=0, sticky='EW')
        self.b_slider.grid(row=4, column=1, columnspan=3, sticky='EW')
        self.b_value_label.grid(row=4, column=4, sticky='EW')
        # Slider container
        self.slider_container.columnconfigure(1, weight=4)
        self.slider_container.columnconfigure(4, minsize=25)
        self.slider_container.grid(row=2, column=0, columnspan=5, padx=padding, sticky='NESW')
        # Buttons for editing tags
        self.add_button.grid(row=5, column=1, padx=padding, pady=padding, sticky='E')
        self.delete_button.grid(row=5, column=2, padx=padding, pady=padding, sticky='EW')
        # Finish and cancel buttons
        self.finish_button.grid(row=5, column=3, padx=padding, pady=padding, sticky='EW')
        self.cancel_button.grid(row=5, column=4, padx=padding, pady=padding, sticky='EW')
        # Master container frame
        self.container.columnconfigure(1, minsize=100)
        self.container.pack(side=LEFT, fill=BOTH)

    @staticmethod
    def truncate(slider):
        """
        Used to truncate slider values since ttk doesn't support the resolution option.
        :return:
        """
        value = slider.get()
        if int(value) != value:
            slider.set(int(value))

    def sort_column(self, col, reverse):
        """
        Sorts the tag list based on a particular column.
        :param col: The column to sort.
        :param reverse: Whether or not to sort in reverse order.
        :return:
        """
        column_elements = [(self.tag_list.set(k, col), k) for k in self.tag_list.get_children('')]
        if col == 'id':
            column_elements = [(int(v), k) for v, k in column_elements]
        column_elements.sort(reverse=reverse)

        for index, (val, k) in enumerate(column_elements):
            self.tag_list.move(k, '', index)

        self.tag_list.heading(col, command=lambda _col=col: self.sort_column(_col, not reverse))

    def callback_update_label(self, var, label):
        """
        Callback used to update the label associated with a slider. Also updates the color associated with the tag.
        :param var: The variable bound to the slider.
        :param label: The label to update.
        :return:
        """
        label.config(text=str(int(var.get())))
        self.update_tag()

    def populate_tags(self, tags):
        """
        Iterates over the tag dictionary and inserts each tag.
        :param tags: A dictionary containing tag, color pairs. The color should be a hex string.
        :return:
        """
        tag_config = ((source, event, color) for source, events in tags.items() for event, color in events.items())
        for source, event, color in tag_config:
            self.insert_tag(source, event, color)

    def insert_tag(self, source, event, color):
        """
        Inserts a tag into the ui and the tag list.
        :param source: The event source.
        :param event: The event id as a string.
        :param color: The color to associate with the tag as a string in hex format.
        :return:
        """
        tag = f'{source}::{event}'
        self.tag_list.insert('', 'end', values=(source, int(event)), tags=(tag,))
        self.tag_list.tag_configure(tag, background=color)
        self.tags[source] = self.tags.get(source, dict())
        self.tags[source][event] = color

    def callback_update_select_background(self, event=None):
        """
        Callback used to update the selection background and sliders to match the selection.
        :return:
        """
        selection = self.tag_list.focus()
        if not selection:
            return
        source, event = (str(v) for v in self.tag_list.item(selection)['values'])
        hex_color = self.tags[source][event]

        # self.color_block.create_rectangle(0, 0, 301, 21, fill=hex_color)
        self.color_block.itemconfigure(self.color_block_rect, fill=hex_color)

        hex_color = hex_color.lstrip('#')
        r, g, b = tuple(int(hex_color[i:i + 2], 16) for i in range(0, 5, 2))
        self.r_slider.set(r)
        self.g_slider.set(g)
        self.b_slider.set(b)

    def update_tag(self):
        """
        Updates the colors associated with a tag
        :return:
        """
        selection = self.tag_list.focus()
        if not selection:
            return
        source, event = (str(v) for v in self.tag_list.item(selection)['values'])
        r, g, b = tuple(map(int, (self.r_slider.get(), self.g_slider.get(), self.b_slider.get())))
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.tags[source][event] = hex_color
        self.color_block.itemconfigure(self.color_block_rect, fill=hex_color)
        self.tag_list.tag_configure('::'.join((source, event)), background=hex_color)
        self.changes_made = True

    def callback_add_tag(self, event=None):
        """
        Creates a dialog window for the user to enter a new tag.
        :return:
        """
        window = TagPrompt(self)
        window.grab_set()

    def callback_remove_tag(self, event=None):
        selection = self.tag_list.focus()
        if not selection:
            return
        source, event = (str(v) for v in self.tag_list.item(selection)['values'])
        self.tags[source].pop(event)
        if len(self.tags[source].keys()) == 0:
            self.tags.pop(source)
        self.tag_list.delete(selection)
        self.changes_made = True

    def callback_finish(self, event=None):
        """
        Callback used to finish making changes to the tags and return to master.
        :return:
        """
        self.master.current_project.config['events'] = self.master.current_project.config.get('events', {})
        self.master.current_project.config['events']['colors'] = self.tags
        if self.master.timeline is not None:
            self.master.timeline.update_tags(self.master.current_project.config['events']['colors'])
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


class TagPrompt(Toplevel):
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
        if event in self.master.tags.get(source, {}):
            messagebox.showerror('Error', 'That tag already exists.')
            return
        self.master.insert_tag(source, event, '#FFFFFF')
        self.master.changes_made = True
        self.destroy()

    def __destroy__(self):
        """
        Returns focus and control to the master.
        :return:
        """
        self.grab_release()
