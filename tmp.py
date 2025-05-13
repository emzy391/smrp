import tkinter as tk
from tkinter import ttk  # Import ttk for styled widgets (like Entry)
import csv
import datetime


def create_window():
    """Создает пустое окно размером с четверть экрана."""
    # 1. Получаем размеры экрана
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    # 2. Вычисляем размеры окна (четверть экрана)
    window_width = screen_width // 2  # Целочисленное деление для получения целого числа
    window_height = screen_height // 2
    # 3. Вычисляем координаты для размещения окна в центре
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    # 4. Устанавливаем размеры и положение окна
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")  # Форматированная строки
    root.title("База данных") # Задаем заголовок окна (необязательно)


    # Frame для поисковой строки (всегда отображается)
    search_frame = tk.Frame(root, bg="#ADD8E6")
    search_frame.pack(pady=(window_height // 16, 0))

    # Поисковая строка
    search_entry = ttk.Entry(search_frame, width=60)
    search_entry.pack(padx=5, pady=5)

    # Стиль поисковой строки
    style_entry = ttk.Style()
    style_entry.configure("TEntry",
                          background="white",
                          foreground="black",
                          fieldbackground="white")
    search_entry['style'] = 'TEntry'

    # Frame для контента (меняется)
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Функция для очистки content_frame
    def clear_content():
        for widget in content_frame.winfo_children():
            widget.destroy()

    def show_main_menu():
        clear_content()

        # Frame для кнопок основного меню
        frame_buttons = tk.Frame(content_frame)
        frame_buttons.pack(pady=0)

        # Стиль для кнопок
        style_button = ttk.Style()
        style_button.configure("My.TButton",
                               font=('Arial', 14),
                               padding=10)

        button_exhibitions = ttk.Button(frame_buttons, text="Выставки", style="My.TButton", width=20,
                                        command=show_exhibitions)
        button_exhibits = ttk.Button(frame_buttons, text="Экспонаты", style="My.TButton", width=20,
                                     command=show_exhibits)
        button_authors = ttk.Button(frame_buttons, text="Авторы", style="My.TButton", width=20, command=show_authors)

        button_exhibitions.pack(pady=5)
        button_exhibits.pack(pady=5)
        button_authors.pack(pady=5)

    def show_exhibitions():
        clear_content()
        root.title("База данных")  # <------ Вот изменение!
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        exhibitions_data = []  # Инициализируем exhibitions_data
        locations = {}  # Инициализируем locations

        # Чтение данных из exhibitions.csv
        try:
            with open("exhibitions.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)
                exhibitions_data = list(reader)
        except FileNotFoundError:
            tk.messagebox.showerror("Ошибка", "Файл exhibitions.csv не найден.")
            return  # Важно выйти из функции, если файл не найден

        # Сортировка выставок по дате начала (от новых к старым)
        try:
            exhibitions_data.sort(key=lambda x: datetime.datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)
        except (ValueError, IndexError) as e:
            tk.messagebox.showerror("Ошибка", f"Ошибка при сортировке выставок: {e}. Проверьте формат дат в файле.")

        # Чтение данных из location.csv
        try:
            with open("location.csv", "r", encoding="utf-8") as file:
                reader = csv.reader(file, delimiter=";")
                next(reader)  # Пропускаем заголовок
                locations = {row[0]: row[1:] for row in
                             reader}  # Создаем словарь {ID: [city, address, organization, phone]}
        except FileNotFoundError:
            tk.messagebox.showerror("Ошибка", "Файл location.csv не найден.")
            return  # Важно выйти из функции, если файл не найден

        # Список выставок
        exhibition_names = [row[1] for row in exhibitions_data]
        num_exhibitions = len(exhibition_names)
        listbox_height = min(num_exhibitions, 10)  # Высота, но не больше 10

        # Frame для Listbox и Scrollbar (используем grid)
        list_frame = tk.Frame(content_frame)
        list_frame.pack(pady=10, fill="both", expand=True)

        listbox_width = 60 if num_exhibitions <= 10 else 40  # Уменьшаем ширину, если > 10
        listbox = tk.Listbox(list_frame, font=('Arial', 12), width=listbox_width, height=listbox_height)

        for name in exhibition_names:
            listbox.insert(tk.END, name)

        # Добавляем Scrollbar, если количество выставок больше 10
        if num_exhibitions > 10:
            scrollbar = tk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
            listbox.configure(yscrollcommand=scrollbar.set)

            # Используем grid для размещения listbox и scrollbar
            listbox.grid(row=0, column=0, sticky="nsew")  # Размещаем listbox в ячейке (0, 0)
            scrollbar.grid(row=0, column=1, sticky="ns")  # Размещаем scrollbar справа от listbox

            # Настраиваем weights для grid, чтобы listbox расширялся
            list_frame.grid_rowconfigure(0, weight=1)
            list_frame.grid_columnconfigure(0, weight=1)  # Разрешаем столбцу с listbox расширяться

            info_label = tk.Label(content_frame, text="", font=('Arial', 10), wraplength=600, justify='left')
            info_label.pack(pady=5)
        else:
            listbox.pack(pady=0)  # Дополнительная информация о выставке
            info_label = tk.Label(list_frame, text="", font=('Arial', 10), wraplength=600, justify='left')
            info_label.pack(pady=10)

        def open_exhibits_window(exhibition_id, exhibition_name):
            show_exhibits_for_exhibition(exhibition_id, exhibition_name)

        def on_listbox_select(event):
            selected_index = listbox.curselection()
            if selected_index:
                selected_exhibition = exhibitions_data[selected_index[0]]
                exhibition_id = selected_exhibition[0]
                # name = selected_exhibition[1]
                start_date_str = selected_exhibition[2]
                end_date_str = selected_exhibition[3]
                location_id = selected_exhibition[4]

                try:
                    start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").strftime("%d.%m.%Y")
                    end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").strftime("%d.%m.%Y")

                    # Проверяем, прошла ли дата завершения выставки
                    end_date_obj = datetime.datetime.strptime(end_date_str, "%Y-%m-%d")
                    if end_date_obj < datetime.datetime.now():
                        archive_status = " (архив)"
                    else:
                        archive_status = ""

                except ValueError:
                    start_date = "Неверный формат даты"
                    end_date = "Неверный формат даты"
                    archive_status = ""  # Или другое значение по умолчанию

                if location_id in locations:
                    location = locations[location_id]
                    city = location[0]
                    address = location[1]
                    organization = location[2]
                    phone = location[3] if location[3] != 'null' else "Не указан"  # Обработка значения null

                    info_text = f"Даты проведения: {start_date} - {end_date}{archive_status}\n" \
                                f"Место: {city}, {organization}\n" \
                                f"Адрес: {address}\n" \
                                f"Телефон: {phone}"
                else:
                    info_text = f"Выставка: {name}\n" \
                                f"Даты проведения: {start_date} - {end_date}{archive_status}\n" \
                                f"Место: Информация о месте не найдена."

                info_label.config(text=info_text)

        # Двойной клик открывает новое окно с экспонатами
        listbox.bind("<Double-Button-1>", lambda event: open_exhibits_window(
            exhibitions_data[listbox.curselection()[0]][0],  # exhibition_id
            exhibitions_data[listbox.curselection()[0]][1]  # exhibition_name
        ))

        listbox.bind("<<ListboxSelect>>", on_listbox_select)

    def show_exhibits_for_exhibition(exhibition_id, exhibition_name):
        """Отображает экспонаты для выбранной выставки в content_frame с прокруткой."""
        clear_content()  # Очищаем content_frame
        root.title(f"{exhibition_name}")  # Изменяем заголовок

        # Кнопка "Назад"
        back_button = ttk.Button(content_frame, text="< Назад", command=show_exhibitions)  # Возврат к show_exhibitions
        back_button.pack(anchor="nw", padx=5, pady=5)

        # Чтение данных из exhibits.csv
        try:
            with open("exhibits.csv", "r", encoding="utf-8") as exhibits_file:
                exhibits_reader = csv.reader(exhibits_file, delimiter=";")
                next(exhibits_reader)  # Пропускаем заголовок
                exhibits_data = [row for row in exhibits_reader if row[0] == exhibition_id]  # фильтр по id выставки
        except FileNotFoundError:
            tk.messagebox.showerror("Ошибка", "Файл exhibits.csv не найден.")
            return

        # Чтение данных из masters.csv
        masters = {}
        try:
            with open("masters.csv", "r", encoding="utf-8") as masters_file:
                masters_reader = csv.reader(masters_file, delimiter=";")
                next(masters_reader)  # Пропускаем заголовок
                masters = {row[0]: row[1] for row in masters_reader}  # Создаем словарь {ID_master: name}
        except FileNotFoundError:
            tk.messagebox.showerror("Ошибка", "Файл masters.csv не найден.")
            return

        # Canvas для прокрутки
        canvas = tk.Canvas(content_frame, highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Frame для размещения экспонатов
        exhibits_frame = tk.Frame(canvas)
        canvas.create_window((0, 0), window=exhibits_frame, anchor="nw")

        # Вывод списка экспонатов
        if exhibits_data:
            for i, exhibit in enumerate(exhibits_data):
                exhibit_name = exhibit[2]
                master_id = exhibit[7]
                master_name = masters.get(master_id,
                                          "Неизвестный автор") if master_id != 'null' else "Неизвестный автор"

                exhibit_info = f"{exhibit_name} - {master_name}"
                exhibit_label = tk.Label(exhibits_frame, text=exhibit_info, font=('Arial', 10), justify='left',
                                         padx=20)  # <--- ИЗМЕНЕНИЕ ТУТ
                exhibit_label.grid(row=i, column=0, sticky="w", pady=2)  # Используем grid для размещения
        else:
            no_exhibits_label = tk.Label(exhibits_frame, text="На этой выставке нет экспонатов.", font=('Arial', 12))
            no_exhibits_label.pack(pady=10)

        # Функция для прокрутки колесиком мыши
        def mouse_scroll(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", mouse_scroll)  # bind для всех виджетов, использующих canvas

    def show_exhibits():
        clear_content()
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        label = tk.Label(content_frame, text="Информация об экспонатах будет здесь.", font=('Arial', 12))
        label.pack(pady=20)
        # Здесь должен быть код для отображения информации об экспонатах

    def show_authors():
        clear_content()
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        label = tk.Label(content_frame, text="Информация об авторах будет здесь.", font=('Arial', 12))
        label.pack(pady=20)
        # Здесь должен быть код для отображения информации об авторах

    # Отображаем основное меню при запуске
    show_main_menu()


root = tk.Tk() # Создаем главное окно Tkinter
create_window() # Вызываем функцию для создания окна
root.mainloop() # Запускаем главный цикл обработки событий (окно будет отображаться, пока программа работает)
