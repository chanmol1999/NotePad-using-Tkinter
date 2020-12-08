import tkinter as tk
import os
import time
import datetime
import tkinter.font as TkFont
from tkinter.messagebox import *
from tkinter.filedialog import *


def newfile(event=None):
    global file
    root.title("New File")
    file = None
    text.delete(1.0, END)


def openfile(event=None):
    global file, file_path
    file = askopenfilename(defaultextension=".txt", filetypes=[
                           ("All Files", "*.*"), ("Text Documents", "*.txt")])
    file_path = file
    if file == "":
        file = None
    else:
        root.title(os.path.basename(file) + " - Notepad")
        text.delete(1.0, END)
        file = open(file, "r")
        text.insert(1.0, file.read())
        file.close()


def savefile(event=None):
    global file, file_path
    if file == None:
        saveasfile()
    else:
        file_name = open(file, "w")
        file_name.write(text.get(1.0, END))
        file_name.close()


def saveasfile(event=None):
    global file, file_path
    if file == None:
        # Save as new file
        file = asksaveasfilename(initialfile='Untitled.txt', defaultextension=".txt", filetypes=[
            ("All Files", "*.*"), ("Text Documents", "*.txt")])
        file_path = file
        if file == "":
            file = None
        else:
            # Try to save the file
            file_name = open(file, "w")
            file_name.write(text.get(1.0, END))
            file_name.close()
            # Change the window title
            root.title("Notepad")
    else:
        file_name = open(file, "w")
        file_name.write(text.get(1.0, END))
        file_name.close()


def cut():
    text.event_generate("<<Cut>>")


def copy():
    text.event_generate("<<Copy>>")


def paste():
    text.event_generate("<<Paste>>")


def find_function(edit):
    text.tag_remove('found', '1.0', END)
    s = edit.get()
    if (s):
        idx = '1.0'
        while 1:
            idx = text.search(s, idx, nocase=1,
                              stopindex=END)

            if not idx:
                break
            lastidx = '% s+% dc' % (idx, len(s))
            text.tag_add('found', idx, lastidx)
            idx = lastidx
        text.tag_config('found', foreground='red', background='yellow')
    edit.focus_set()


def findNreplace(edit, edit2):
    text.tag_remove('found', '1.0', END)

    s = edit.get()
    r = edit2.get()

    if (s and r):
        idx = '1.0'
        while 1:
            idx = text.search(s, idx, nocase=1,
                              stopindex=END)
            if not idx:
                break
            lastidx = '% s+% dc' % (idx, len(s))

            text.delete(idx, lastidx)
            text.insert(idx, r)

            lastidx = '% s+% dc' % (idx, len(r))

            text.tag_add('found', idx, lastidx)
            idx = lastidx
        text.tag_config('found', foreground='green', background='yellow')
    edit.focus_set()


def exit(find_root):
    text.tag_remove('found', '1.0', END)
    find_root.destroy()


def find(event=None):
    find_root = Toplevel(root)
    find_root.title('FindNReplace')
    fram = Frame(find_root)

    Label(fram, text='Find').pack(side=LEFT)
    edit = Entry(fram)
    edit.pack(side=LEFT, fill=BOTH, expand=1)
    Find = Button(fram, text='Find')
    Find.pack(side=LEFT)

    Label(fram, text="Replace With ").pack(side=LEFT)
    edit2 = Entry(fram)
    edit2.pack(side=LEFT, fill=BOTH, expand=1)
    edit.focus_set()
    replace = Button(fram, text='FindNReplace')
    replace.pack(side=LEFT)

    Exit = Button(fram, text='Exit')
    Exit.pack(side=LEFT)

    fram.pack(side=TOP)

    Find.config(command=lambda: find_function(edit))
    replace.config(command=lambda: findNreplace(edit, edit2))
    Exit.config(command=lambda: exit(find_root))
    find_root.mainloop()


def word_count():
    data = text.get("1.0", 'end-1c')
    words = data.split()
    return str(len(words))


def char_count():
    return str(len(text.get("1.0", 'end-1c')))


def created_time():
    if file != None:
        modificationTime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(os.path.getctime(str(file_path))))
        tk.messagebox.showinfo('Created time',
                               'Created at: ' + str(modificationTime))


def modified_time():
    if file != None:
        modificationTime = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(os.path.getmtime(str(file_path))))
        tk.messagebox.showinfo('Modified time',
                               'Last Modified at: ' + str(modificationTime))


def change(clicked_font_size, clicked_font, font_root):
    global text, font_family, font_size
    font_family = clicked_font.get()
    font_size = clicked_font_size.get()
    font_custom = TkFont.Font(size=font_size, family=font_family)
    text.configure(font=font_custom)
    font_root.destroy()


def font():
    font_root = Toplevel(root)
    font_root.title('Select Font')
    font_root.geometry('300x120')
    options = [
        'System',
        'Terminal',
        'Fixedsys',
        'Modern',
        'Roman',
        'Script',
        'Courier',
        'MS Serif',
        'MS Sans Serif',
        'Small Fonts',
        'Marlett',
        'Arial',
        'Arabic Transparent',
        'Arial Baltic',
        'Calibri',
        'Calibri Light',
        'Cambria',
        'Cambria Math',
        'Candara',
        'Candara Light',
        'Comic Sans MS',
        'Consolas',
        'Constantia',
        'Franklin Gothic Medium',
        'Gabriola',
        'Leelawadee UI Semilight',
        'Lucida Console',
        'MV Boli',
        'Sylfaen',
        'Symbol',
        'Tahoma',
        'Times New Roman',
        'Times New Roman Baltic',
        'Trebuchet MS',
        'Verdana',
        'Webdings',
        'Wingdings',
        'Ubuntu Condensed',
        'Ubuntu Light'
    ]
    options_font_size = [
        '1', '3', '4', '5', '6', '7', '9', '10', '12', '14', '16', '18', '20', '21', '22', '24', '26', '28', '30']
    clicked_font = StringVar()
    clicked_font_size = StringVar()
    clicked_font.set(font_family)
    clicked_font_size.set(font_size)
    drop_font = OptionMenu(font_root, clicked_font, *options)
    drop_font.pack(side=LEFT)
    drop_font_size = OptionMenu(
        font_root, clicked_font_size, *options_font_size)
    drop_font_size.pack(side=LEFT)
    Button(font_root, text="Ok",
           command=lambda: change(clicked_font_size, clicked_font, font_root)).pack(side=RIGHT)


def exit_main(event=None):
    root.destroy()


def about():
    tk.messagebox.showinfo('About Notepad',
                           'This notepad is developed by Anmol Chaddha and Apoorv Verma as their academic project for CS384 - Introduction to Python under professor Dr. Mayank Agarwal.')


def highlight(event=None):
    global text
    try:
        text.tag_add("start", "sel.first", "sel.last")
    except tk.TclError:
        pass


def clear():
    global text
    text.tag_remove("start",  "1.0", 'end')


def status_bar_update(event=None):
    global statusbar
    statusbar.config(text="Word count: " + word_count() +
                     '| Char: ' + char_count())


file = None
file_path = None
root = Tk()
root.geometry('500x500')
root.title('Duo.py')
text = Text(root)
font_family = 'Arial'
font_size = 14
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
text.grid(sticky=N + E + S + W, pady=10)
menuBar = Menu(root)
root.config(menu=menuBar)
font_custom = TkFont.Font(size=font_size, family=font_family)
text.configure(font=font_custom)
text.tag_configure("start", background="yellow")

FileMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="File", menu=FileMenu)
FileMenu.add_command(label='New', command=newfile, accelerator="Ctrl+N")
root.bind('<Control_L><N>', newfile)
root.bind('<Control_L><n>',  newfile)
FileMenu.add_command(label='Open', command=openfile, accelerator="Ctrl+O")
root.bind('<Control_L><o>', openfile)
root.bind('<Control_L><O>',  openfile)
FileMenu.add_separator()
FileMenu.add_command(label='Save', command=savefile, accelerator="Ctrl+S")
root.bind('<Control_L><s>', savefile)
root.bind('<Control_L><S>',  savefile)
FileMenu.add_command(label='Save As', command=saveasfile, accelerator="Ctrl+S")
FileMenu.add_separator()
FileMenu.add_command(label='Exit', command=exit_main, accelerator="Ctrl+Q")
root.bind('<Control_L><q>', exit_main)
root.bind('<Control_L><Q>',  exit_main)
FileMenu.add_separator()

EditMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Edit", menu=EditMenu)
EditMenu.add_command(label='Cut', command=cut, accelerator="Ctrl+X")
EditMenu.add_command(label='Copy', command=copy, accelerator="Ctrl+C")
EditMenu.add_command(label='Paste', command=paste, accelerator="Ctrl+V")
EditMenu.add_separator()
EditMenu.add_command(label='FindNReplace', command=find, accelerator="Ctrl+F")
root.bind('<Control_L><f>', find)
root.bind('<Control_L><F>',  find)
EditMenu.add_separator()

StatsMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Stats", menu=StatsMenu)
StatsMenu.add_command(label='Created Time', command=created_time)
StatsMenu.add_command(label='Modified Time', command=modified_time)
StatsMenu.add_separator()

CustomiseMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Format", menu=CustomiseMenu)
CustomiseMenu.add_command(label='Font', command=font)
CustomiseMenu.add_separator()
CustomiseMenu.add_command(
    label='Highlight', command=highlight, accelerator="Ctrl+H")
root.bind('<Control_L><h>', highlight)
root.bind('<Control_L><H>',  highlight)
CustomiseMenu.add_command(label='Clear', command=clear)
CustomiseMenu.add_separator()

HelpMenu = Menu(menuBar, tearoff=0)
menuBar.add_cascade(label="Help", menu=HelpMenu)
HelpMenu.add_command(label='About', command=about)
HelpMenu.add_separator()

scrollBar = Scrollbar(text)
scrollBar.pack(side=RIGHT, fill=Y)
scrollBar.config(command=text.yview)
text.config(yscrollcommand=scrollBar.set)

statusbar = tk.Label(root, text="Word count: " + word_count() + '| Char: ' + char_count(), bd=5,
                     relief=tk.SUNKEN, anchor=tk.W)
statusbar.grid(sticky=S + E, pady=2)
root.bind("<Key>", status_bar_update)

root.mainloop()
