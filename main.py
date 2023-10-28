import tkinter as tk 
from tkinter import ttk
import sqlite3, os


# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)   
        self.init_main()
        self.db = db
        self.view_records()

    #Создание и работа с главным окном
    def init_main(self):
        toolbar = tk.Frame(bg = '#d7d7d7', bd = 2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

#Buttoms
        
        dir = os.path.dirname(__file__)

        # Добавить
        self.add_img = tk.PhotoImage(file=dir + '/img/add.png')
        btn_add = tk.Button(toolbar,bg='#d7d7d7', bd=2, image = self.add_img, command = self.open_child)
        btn_add.pack(side=tk.LEFT)
        
        # обновить
        self.upd_img = tk.PhotoImage(file=dir + '/img/update.png')
        btn_upd = tk.Button(toolbar, bg='#d7d7d7', bd=3, image = self.upd_img, command = self.open_update_dialog)
        btn_upd.pack(side = tk.LEFT)
        
        # Удалить
        self.del_img = tk.PhotoImage(file=dir + '/img/delete.png')
        btn_del = tk.Button(toolbar, bg='#d7d7d7', bd=4,
                            image = self.del_img, command = self.delite_records)
        btn_del.pack(side = tk.LEFT)
        
        #Поиск
        self.search_img = tk.PhotoImage(file=dir + '/img/search.png')
        btn_search = tk.Button(toolbar, bg='#d7d7d7', bd=5,
                            image = self.search_img, command = self.open_search)
        btn_search.pack(side = tk.LEFT)
        
        #Обновить
        self.refresh_img = tk.PhotoImage(file=dir + '/img/refresh.png')
        btn_refrash = tk.Button(toolbar, bg='#d7d7d7', bd=6,
                            image = self.refresh_img, command = self.view_records)
        btn_refrash.pack(side = tk.LEFT)
        
#Таблица

        #Добавляем таблицы
        self.tree = ttk.Treeview(self, columns=('ID', 'name', 'phone', 'email','zp'),
                                height=45, show = 'headings')

        # Добавить параметры колонкам
        self.tree.column('ID', width=45, anchor=tk.CENTER)
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('phone', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('zp', width=150, anchor=tk.CENTER)

        # Подписи колонок
        self.tree.heading("ID", text="ID")
        self.tree.heading("name", text="ФИО")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")
        self.tree.heading("zp", text="Зарплата")

        # Упаковка
        self.tree.pack(side=tk.LEFT)

#Методы

    # метод для добавления данных
    def records(self, name, phone, email, zp):
        self.db.insert_data(name,phone,email, zp)
        self.view_records()
        
    # отображение данных в TreeView
    def view_records(self):
        self.db.cur.execute('''SELECT * FROM users''')

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]
      
    # метод для обновления данных
    def update_record(self, name, phone, email, zp):
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cur.execute('''UPDATE users SET name=?, phone=?, email=?, zp=? WHERE ID=?''',
                            (name, phone, email, id, zp))
        self.db.conn.commit()
        self.view_records()
      
    # метод для удаления данных
    def delite_records(self):
        for row in self.tree.selection():
            self.db.cur.execute('''DELETE FROM users WHERE ID=?''',
                                (self.tree.set(row, '#1'),))
        self.db.conn.commit()
        self.view_records()
      
    # метод для поиска данных
    def search_records(self, name):
        name = ('%'+ name +'%')
        self.db.cur.execute('''SELECT * FROM users WHERE name LIKE ?''', (name, ))
          
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.cur.fetchall()]

#Вызов классов
    # метод вызывающий окно добавления
    def open_child(self):
        Child()
        
    # метод вызывающий окно обновления
    def open_update_dialog(self):
        Update()
        
    # метод вызывающий окно поиска
    def open_search(self):
        Search()

# Создание дочерних окон
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    # Создание и работа с дочерним окном
    def init_child(self):
        self.title("Добавить сотрудника")
        self.geometry('400x200')
        # перехватываем все события происходящие в приложении
        self.grab_set()
        # захватываем фокус
        self.focus_set()
        # размещаем элименты в окне
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=50, y=50)

        label_phone = tk.Label(self, text='Тел: ')
        label_phone.place(x=50, y=80)

        label_email = tk.Label(self, text='Email: ')
        label_email.place(x=50, y=110)

        label_zp = tk.Label(self, text='Зарплата: ')
        label_zp.place(x=50, y=140)


        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=200, y=50)

        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x=200, y=80)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=110)
        
        self.entry_zp = ttk.Entry(self)
        self.entry_zp.place(x=200, y=140)

        # кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=300, y=170)
        
        # кнопка добавления
        self.btn_add = ttk.Button(self, text='Добавить')
        self.btn_add.place(x=220, y=170)
        self.btn_add.bind('<Button-1>', lambda event:
                            self.view.records(self.entry_name.get(),
                            self.entry_phone.get(),
                            self.entry_email.get(),
                            self.entry_zp.get()))

# класс редактирования контактов
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_update()
        self.db = db
        self.default_data()
        
    def init_update(self):
        self.title('Редактировать сотрудника')
        self.btn_add.destroy()
         
        self.btn_upd = ttk.Button(self, text='Редактировать')
        self.btn_upd.bind('<Button-1>', lambda event:
                            self.view.update_record(self.entry_name.get(),
                            self.entry_phone.get(),
                            self.entry_email.get(),
                            self.entry_zp.get()))
        self.btn_upd.bind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_upd.place(x=200, y=170)
          
    def default_data(self):
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cur.execute('''SELECT * FROM users WHERE ID=?''', (id, ))
         
        row = self.db.cur.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_zp.insert(0, row[4])

# Класс поиска
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app
        
        
    def init_child(self):
        self.title('Поиск сотрудника')
        self.geometry('300x100')
        self.resizable(False, False)
        self.grab_set()
        self.focus_set()
        
        # label и само поле для поиска
        label_name = tk.Label(self, text='ФИО: ')
        label_name.place(x=20, y=20)
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x=70, y=20)

         # кнопка закрытия
        self.btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.btn_cancel.place(x=200, y=70)
        
         # кнопка поиска
        self.btn_search = ttk.Button(self, text='Искать', command=self.destroy)
        self.btn_search.place(x=70, y=70)
        self.btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_name.get()))

# класс базы данных
class DB:
    def __init__(self):
        dir = os.path.dirname(__file__)
        self.conn = sqlite3.connect(dir+'/contacts.db')
        self.cur = self.conn.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY NOT NULL,
                                name TEXT,
                                phone TEXT,
                                email TEXT,
                                zp TEXT )''')
        self.conn.commit()
         
    def insert_data (self, name, phone, email, zp):
        self.cur.execute('''INSERT INTO users (
                                name, phone, email, zp) VALUES (?, ?, ?, ?)''', (name, phone, email, zp))
        self.conn.commit()

# Создание окна 
if __name__ == '__main__':         
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Книга сотрудников')
    root.geometry('800x600')
    root.resizable(False, False)
    root.configure(bg = 'White')
    root.mainloop()