#!/usr/bin/env python3

import os
import sys
import tkinter as tk

TITLE = "Roomthon"

class Roomthon(tk.Text):
    def __init__(self, master, **options):
        tk.Text.__init__(self, master, **options)

        self.config(borderwidth=0,
                    font="-xos4-terminus-medium-r-normal--14-140-72-72-c-80-iso8859-15",
                    foreground="#71c293",
                    background="#06544a",
                    insertbackground="white", # cursor
                    selectforeground="#06544a", # selection
                    selectbackground="#71c293",
                    wrap=tk.WORD, # use word wrapping
                    undo=True,
                    width=10000,
                    insertofftime=0)

    def _getfilename(self):
        return self._filename

    def _setfilename(self, filename):
        self._filename = filename
        title = os.path.basename(filename or "(new document)")
        title = title + " - " + TITLE
        self.winfo_toplevel().title(title)

    filename = property(_getfilename, _setfilename)

    def edit_modified(self, value=None):
        return self.tk.call(self, "edit", "modified", value)

    modified = property(edit_modified, edit_modified)

    def load(self, filename):
        text = open(filename).read()
        self.delete(1.0, tk.END)
        self.insert(tk.END, text)
        self.mark_set(tk.INSERT, 1.0)
        self.modified = False
        self.filename = filename
        self.edit_reset()

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        f = open(filename, "w")
        s = self.get(1.0, tk.END)
        try:
            f.write(s.rstrip())
            f.write("\n")
        finally:
            f.close()
        self.modified = False
        self.filename = filename

root = tk.Tk()
root.config(background="black")

root.wm_state("normal")

editor = Roomthon(root)
editor.pack(fill=tk.Y, expand=1)

editor.focus_set()

FILETYPES = [
    ("Text files", "*.txt"), ("All files", "*")
]

class Cancel(Exception):
    pass

def open_as():
    from tkinter.filedialog import askopenfilename
    f = askopenfilename(parent=root, filetypes=FILETYPES)
    if not f:
        raise Cancel
    try:
        editor.load(f)
    except IOError:
        from tkinter.messagebox import showwarning
        showwarning("Open", "Cannot open the file.")
        raise Cancel

def save_as():
    from tkinter.filedialog import asksaveasfilename
    f = asksaveasfilename(parent=root, defaultextension=".txt")
    if not f:
        raise Cancel
    try:
        editor.save(f)
    except IOError:
        from tkinter.messagebox import showwarning
        showwarning("Save As", "Cannot save the file.")
        raise Cancel

def save():
    if editor.filename:
        try:
            editor.save(editor.filename)
        except IOError:
            from tkinter.messagebox import showwarning
            showwarning("Save", "Cannot save the file.")
            raise Cancel
    else:
        save_as()

def save_if_modified():
    if not editor.modified:
        return
    if askyesnocancel(TITLE, "Document modified. Save changes?"):
        save()

def askyesnocancel(title=None, message=None, **options):
    import tkinter.messagebox
    s = tkinter.messagebox.Message(title=title, message=message,
                                   icon=tkinter.messagebox.QUESTION,
                                   type=tkinter.messagebox.YESNOCANCEL,
                                   **options).show()
    if isinstance(s, bool):
        return s
    if s == "cancel":
        raise Cancel
    return s == "yes"

def file_open(event=None):
    try:
        save_if_modified()
        open_as()
    except Cancel:
        pass
    return "break"

def file_save(event=None):
    try:
        save()
    except Cancel:
        pass
    return "break"

def file_save_as(event=None):
    try:
        save_as()
    except Cancel:
        pass
    return "break"

def file_quit(event=None):
    try:
        save_if_modified()
    except Cancel:
        return
    root.quit()

editor.bind("<Control-o>", file_open)
editor.bind("<Control-s>", file_save)
editor.bind("<Control-Shift-S>", file_save_as)
editor.bind("<Control-q>", file_quit)

root.protocol("WM_DELETE_WINDOW", file_quit) # window close button

try:
    editor.load(sys.argv[1])
except (IndexError, IOError):
    pass

tk.mainloop()
