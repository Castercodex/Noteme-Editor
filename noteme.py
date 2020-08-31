import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os

root = tk.Tk()
file_name =  None

#functions
def saveasfile(event=None):
    input_file_name = tk.filedialog.asksaveasfilename(initialdir='/', title='Save File', filetypes=(
    ('Text Documents', '*.txt'), ('All files', '*.*')))
    if input_file_name:
        global file_name
        file_name = input_file_name
        write_to_file(file_name)
        root.title('{}'.format(os.path.basename(file_name)))
    return "break"

def savefile(event=None):
    global file_name
    if not file_name:
        saveasfile()
    else:
        write_to_file(file_name)
    return "break"

def on_change_text(event=None):
    update_line_numbers()

def openfile(event=None):
    input_file_name = filedialog.askopenfilename(initialdir='/', title='Open File', filetypes=(('Text Documents', '*.txt'),('All files', '*.*')))
    if input_file_name:
        global file_name
        file_name = input_file_name
        root.title('{}'.format(os.path.basename(file_name)))
        textfield.delete(1.0, 'end')
    with open(file_name) as _file:
        textfield.insert(1.0, _file.read())
        on_change_text()

def newfile(event=None):
    root.title("Untitled")
    global file_name
    file_name = None
    textfield.delete(1.0,'end')


def write_to_file(file_name):
    try:
        content = textfield.get(1.0, 'end')
        with open(file_name, 'w') as the_file:
            the_file.write(content)
    except IOError:
        pass

def get_line_numbers():
    output = ''
    row, col = textfield.index("end").split('.')
    for i in range(1, int(row)):
        output += str(i)+ '\n'
    return output

def update_line_numbers(event = None):
    line_numbers = get_line_numbers()
    lineNumberBar.config(state='normal')
    lineNumberBar.delete('1.0', 'end')
    lineNumberBar.insert('1.0', line_numbers)
    lineNumberBar.config(state='disabled')

def exit(event=None):
    global file_name
    if file_name:
        root.destroy()
    else:
        tk.messagebox.showwarning('Warning', 'Content Not Saved')
        savefile()



#THE MENUBAR
myMenu = tk.Menu(root)
# Adding Menubar in the widget
menuBar = tk.Menu(root)
fileMenu = tk.Menu(menuBar, tearoff=0)
editMenu = tk.Menu(menuBar, tearoff=0)
viewMenu = tk.Menu(menuBar, tearoff=0)
aboutMenu = tk.Menu(menuBar, tearoff=0)

# all file menu-items will be added here next
menuBar.add_cascade(label='File', menu=fileMenu)
menuBar.add_cascade(label='Edit', menu=editMenu)
menuBar.add_cascade(label='View', menu=viewMenu)
menuBar.add_cascade(label='About', menu=aboutMenu)

fileMenu.add_command(label="New", accelerator='Ctrl + N', compound='left', command=newfile)
fileMenu.add_command(label="Open", accelerator='Ctrl + O', compound='left', command=openfile)
fileMenu.add_command(label="Save", accelerator='Ctrl + S', compound='left', command=savefile)
fileMenu.add_command(label="Save as", accelerator='Ctrl + Shift + S', compound='left', command=saveasfile)
root.config(menu=menuBar)

#frame
frame = tk.Frame(root,bg='#000')
frame.pack(fill='x', ipady=10)
lineNumberBar = tk.Text(root, width=6,  takefocus=0, border=0, background='#cbc6c6', state='disabled')
lineNumberBar.pack(side='left', fill='y')

#Buttons
newfileBtn = tk.Button(frame, text='New File', bg="#4dec4d", height=2, width=10, borderwidth=0, command=newfile)
newfileBtn.pack(side='left')
savefileBtn = tk.Button(frame, text='Save File', bg='#00a6ff',height=2, width=10, borderwidth=0, command=savefile)
savefileBtn.pack(side='left', padx=10)
openfileBtn = tk.Button(frame, text='Open File', bg='#ecc64d',height=2, width=10, borderwidth=0, command=openfile)
openfileBtn.pack(side='left')
#Textarea
textfield = tk.Text(root, bg='#fff', fg='#000', wrap='word', undo=1)
textfield.pack(expand='yes', fill='both')

#Scrollbars
scrollBar = tk.Scrollbar(textfield)
textfield.configure(yscrollcommand=scrollBar.set)
scrollBar.config(command=textfield.yview)
scrollBar.pack(side='right', fill='y')
lineNumberBar.configure(yscrollcommand=scrollBar.set)
#Binding the keyboard shortcuts to function
textfield.bind('<Control-s>', savefile)
textfield.bind('<Control-o>', openfile)
textfield.bind('<Control-n>', newfile)
textfield.bind('<Control-Shift-s>', saveasfile)
textfield.bind('<Control-Shift-S>', saveasfile)
textfield.bind('<Any-KeyPress>', on_change_text)



root.protocol('WM_DELETE_WINDOW', exit)
root.title("NoteME")
root.minsize(1000,500)
root.mainloop()