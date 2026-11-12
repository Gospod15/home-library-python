import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

win = Tk()
win.title("Домашня бібліотека")
win.geometry("750x400") 

database = sqlite3.connect("my_database.db")
cursor = database.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        year INTEGER,
        author_id INTEGER
    )
''')
database.commit()


left_frame = Frame(win, padx=20, pady=20)
left_frame.pack(side=LEFT, fill=Y)
right_frame = Frame(win, padx=20, pady=20)
right_frame.pack(side=RIGHT, fill=BOTH, expand=True)

Label(left_frame, text="Назва книги:").pack(pady=(10,0))
titleT = Entry(left_frame, width=25)
titleT.pack()
Label(left_frame, text="Рік видання:").pack(pady=(10,0))
yearT = Entry(left_frame, width=25)
yearT.pack()
Label(left_frame, text="ID автора:").pack(pady=(10,0))
author_idT = Entry(left_frame, width=25)
author_idT.pack()

tree_scroll = Scrollbar(right_frame)
tree_scroll.pack(side=RIGHT, fill=Y)
tree = ttk.Treeview(right_frame, columns=( 'Author','Title', 'Year',), show='headings', yscrollcommand=tree_scroll.set)

tree.heading('Title', text='Назва книги')
tree.heading('Year', text='Рік')
tree.heading('Author', text='ID Автора')
tree.column('Title', width=200)
tree.column('Year', width=80, anchor=CENTER)
tree.column('Author', width=80, anchor=CENTER)

tree.pack(fill=BOTH, expand=True)
tree_scroll.config(command=tree.yview)

def load_books():
    for item in tree.get_children():
        tree.delete(item)
        
    cursor.execute("SELECT * FROM Books")
    for row in cursor.fetchall():
        tree.insert('', 'end', iid=row[0], values=(row[3], row[1], row[2]))

def add_book():
    title = titleT.get()
    year = yearT.get()
    author_id = author_idT.get()
    
    if not title:
        messagebox.showwarning("Помилка", "Введіть назву книги")
        return

    cursor.execute('''
        INSERT INTO Books (title, year, author_id) 
        VALUES (?, ?, ?)
    ''', (title, year, author_id))
    database.commit()
    
    titleT.delete(0, END)
    yearT.delete(0, END)
    author_idT.delete(0, END)
    
    load_books()

def delete_book():
    selected_item = tree.selection() 
    if not selected_item:
        messagebox.showinfo("Увага", "Оберіть книгу для видалення зі списку")
        return
        
    book_id = selected_item[0]
    cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))
    database.commit()
    
    load_books()

butADD = Button(left_frame, text='Додати книгу', command=add_book)
butADD.pack(pady=20, fill=X)
butDEL = Button(left_frame, text='Видалити обрану книгу', command=delete_book)
butDEL.pack(pady=10)

def print_main_message():
    print("Hello from main branch!")

def print_greetings():
    print("Hello from new-feature branch!")


load_books()
win.mainloop()
database.close()