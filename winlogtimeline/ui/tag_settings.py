from tkinter import *
from tkinter.ttk import *
import re


class TagSettings(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)

        # Class variables
        self.tags = dict()

        # Window Parameters
        self.title('Project Settings')
        self.resizable(width=False, height=False)

        # Create and place the widgets
        self._init_widgets()
        self.populate_tags(parent.current_project.config['events'])
        self._place_widgets()

    def _init_widgets(self):
        """
        Creates the elements of this window and sets configuration values.
        :return:
        """
        # Master container frame
        self.container = Frame(self)
        # Listbox for tags
        self.listbox_container = Frame(self.container)
        self.tag_list = Listbox(self.listbox_container)
        self.tag_list.bind('<<ListboxSelect>>', self.callback_update_select_background)
        self.vsb = Scrollbar(self.listbox_container, orient='vertical', command=self.tag_list.yview)
        # Buttons for editing tags
        self.add_button = Button(self.container, text='Add', command=self.callback_add_tag)
        self.delete_button = Button(self.container, text='Delete', command=self.callback_remove_tag)
        # Red config
        self.red = IntVar()
        self.r_slider = Scale(self.container, from_=0, to=255, variable=self.red,
                              command=lambda *args: self.truncate(self.r_slider))
        self.r_label = Label(self.container, text='0')
        self.red.trace('w', lambda *args: self.callback_update_label(self.red, self.r_label))
        # Green config
        self.green = IntVar()
        self.g_slider = Scale(self.container, from_=0, to=255, variable=self.green,
                              command=lambda *args: self.truncate(self.g_slider))
        self.g_label = Label(self.container, text='0')
        self.green.trace('w', lambda *args: self.callback_update_label(self.green, self.g_label))
        # Blue config
        self.blue = IntVar()
        self.b_slider = Scale(self.container, from_=0, to=255, variable=self.blue,
                              command=lambda *args: self.truncate(self.b_slider))
        self.b_label = Label(self.container, text='0')
        self.blue.trace('w', lambda *args: self.callback_update_label(self.blue, self.b_label))
        # Finish and cancel buttons
        self.finish_button = Button(self.container, text='Finish', command=self.callback_finish)
        self.cancel_button = Button(self.container, text='Cancel', command=self.callback_cancel)

    def _place_widgets(self):
        """
        Lays out the elements in this window.
        :return:
        """
        padding = 3
        # Listbox for tags
        self.tag_list.grid(row=0, column=0, columnspan=3, sticky='NESW')
        self.vsb.grid(row=0, column=3, columnspan=1, sticky='NESW')
        self.listbox_container.columnconfigure(0, weight=4)
        self.listbox_container.grid(row=0, column=0, columnspan=4, padx=padding, pady=padding, sticky='NESW')
        # Buttons for editing tags
        self.add_button.grid(row=1, column=1, padx=padding, pady=padding, sticky='E')
        self.delete_button.grid(row=1, column=2, columnspan=2, padx=padding, pady=padding, sticky='E')
        # Red config
        self.r_slider.grid(row=2, column=0, columnspan=3, padx=padding, sticky='EW')
        self.r_label.grid(row=2, column=3, padx=padding, sticky='E')
        # Green config
        self.g_slider.grid(row=3, column=0, columnspan=3, padx=padding, sticky='EW')
        self.g_label.grid(row=3, column=3, padx=padding, sticky='E')
        # Blue config
        self.b_slider.grid(row=4, column=0, columnspan=3, padx=padding, sticky='EW')
        self.b_label.grid(row=4, column=3, padx=padding, sticky='E')
        # Finish and cancel buttons
        self.finish_button.grid(row=5, column=1, padx=padding, pady=padding, sticky='E')
        self.cancel_button.grid(row=5, column=2, padx=padding, pady=padding, columnspan=2, sticky='E')
        # Master container frame
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
        for tag, color in tags.items():
            self.insert_tag(tag, color)

    def insert_tag(self, tag, color):
        """
        Inserts a tag into the ui and the tag list.
        :param tag: The tag to insert
        :param color: The color to associate with the tag as a string in hex format.
        :return:
        """
        self.tag_list.insert('end', tag)
        self.tag_list.itemconfig('end', bg=color)
        self.tags[tag] = color

    def callback_update_select_background(self, event=None):
        """
        Callback used to update the selection background and sliders to match the selection.
        :return:
        """
        selection = self.tag_list.curselection()
        tag = self.tag_list.get(selection[0])
        hex_color = self.tags[tag]
        self.tag_list.config(selectbackground=hex_color)
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
        selection = self.tag_list.curselection()
        tag = self.tag_list.get(selection[0])
        r, g, b = tuple(map(int, (self.r_slider.get(), self.g_slider.get(), self.b_slider.get())))
        hex_color = f'#{r:02x}{g:02x}{b:02x}'
        self.tags[tag] = hex_color
        self.tag_list.config(selectbackground=hex_color)

    def callback_add_tag(self):
        """
        Creates a dialog window for the user to enter a new tag.
        :return:
        """
        window = TagPrompt(self)
        window.grab_set()

    def callback_remove_tag(self):
        selection = self.tag_list.curselection()
        tag = self.tag_list.get(selection[0])
        self.tags.pop(tag)
        self.tag_list.delete(selection[0])

    def callback_finish(self, event=None):
        """
        Callback used to finish making changes to the tags and return to master.
        :param event:
        :return:
        """
        self.master.current_project.config['events'] = self.tags
        if self.master.timeline is not None:
            self.master.timeline.update_tags(self.tags)
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
        self.id_label = Label(self.container, text='Event ID')
        id_vcmd = (self.container.register(self.validate_command_id), '%d', '%P')
        self.id_entry = Entry(self.container, validate='key', validatecommand=id_vcmd)
        self.ok_button = Button(self.container, text='Ok', command=self.callback_ok)

    def _place_widgets(self):
        padding = 3
        self.id_label.grid(row=0, column=0, columnspan=3, padx=padding, sticky='EW')
        self.id_entry.grid(row=1, column=0, columnspan=3, padx=padding, sticky='EW')
        self.ok_button.grid(row=4, column=2, padx=padding, sticky='NESW')
        self.container.pack()

    @staticmethod
    def validate_command_id(action, value):
        """
        Restricts entry to only allow numbers.
        :return:
        """
        if action != '1':
            return True
        if re.match(r'^[0-9]+$', value):
            return True
        return False

    def callback_ok(self):
        self.master.insert_tag(self.id_entry.get(), '#FFFFFF')
        self.destroy()

    def __destroy__(self):
        """
        Returns focus and control to the master.
        :return:
        """
        self.grab_release()
