import csv
import tkinter as tk
from tkinter import ttk  # Import ttk for styled widgets (like Entry)
import datetime
import tkinter.font as tkFont


# Глобальные переменные для хранения данных
exhibitions_data = []
locations = {}
exhibits_DATA = []
masters = {}
materials = {}

def load_data():
    global exhibitions_data, locations, exhibits_DATA, masters, materials

    try:
        with open("exhibitions.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            exhibitions_data = list(reader)
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", "Файл exhibitions.csv не найден.")
        return

    try:
        with open("location.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            locations = {row[0]: row[1:] for row in reader}
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", "Файл location.csv не найден.")
        return

    try:
        with open("exhibits.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            exhibits_DATA = list(reader)
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", "Файл exhibits.csv не найден.")
        return

    try:
        with open("masters.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            masters = {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", "Файл masters.csv не найден.")
        return

    try:
        with open("materials.csv", "r", encoding="utf-8") as file:
            reader = csv.reader(file, delimiter=";")
            next(reader)
            materials = {row[0]: row[1] for row in reader}
    except FileNotFoundError:
        tk.messagebox.showerror("Ошибка", "Файл materials.csv не найден.")
        return

def clear_content():
    """Очищает content_frame."""
    for widget in content_frame.winfo_children():
        widget.destroy()


def search():
    """Выполняет поиск по данным и отображает результаты."""
    query = search_entry.get().lower()
    clear_content()

    results = []

    # Поиск по выставкам
    exhibition_ids = set()
    for exhibition in exhibitions_data:
        if query in exhibition[1].lower():  # Ищем по названию выставки
            if exhibition[0] not in exhibition_ids:
                results.append({"type": "exhibition", "id": exhibition[0], "name": exhibition[1]})
                exhibition_ids.add(exhibition[0])

    # Поиск по экспонатам
    exhibit_ids = set()
    for exhibit in exhibits_DATA:
        if query in exhibit[2].lower():
            exhibit_id = exhibit[1]
            if exhibit_id not in exhibit_ids:
                results.append({"type": "exhibit", "id": exhibit_id, "name": exhibit[2]})
                exhibit_ids.add(exhibit_id)

    # Поиск по мастерам
    master_ids = set()
    for master_id, master_name in masters.items():
        if query in master_name.lower():  # Ищем по имени мастера
            if master_id not in master_ids:  # Проверка на дубликат
                results.append({"type": "master", "id": master_id, "name": master_name})
                master_ids.add(master_id)  # Добавляем master_id в set

    # Поиск по материалам
    material_exhibit_ids = set()  # Создаем новый set для поиска по материалам
    for exhibit in exhibits_DATA:
        material_ids = exhibit[6].split(',')
        for material_id in material_ids:
            if material_id in materials and query in materials[material_id].lower():
                exhibit_id = exhibit[1]
                if exhibit_id not in material_exhibit_ids:
                    results.append({"type": "exhibit", "id": exhibit_id, "name": exhibit[2]})
                    material_exhibit_ids.add(exhibit_id)

        # Canvas для прокрутки
    print(f"Найдено результатов: {len(results)}")  # Для отладки

    # Основной контейнер
    main_frame = tk.Frame(content_frame)
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Canvas и Scrollbar
    canvas = tk.Canvas(main_frame, highlightthickness=0)
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)

    scrollbar.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Фрейм для результатов
    results_frame = tk.Frame(canvas)
    canvas.create_window((0, 0), window=results_frame, anchor="nw")

    if results:
        for result in results:
            # Создаем обработчик для каждой кнопки
            def make_handler(r):
                return lambda: (
                    show_exhibition_details(r["id"]) if r["type"] == "exhibition" else
                    show_exhibit_details(r["id"]) if r["type"] == "exhibit" else
                    show_master_details(r["id"])
                )

            # Определяем текст для кнопки
            type_text = {
                "exhibition": "Выставка",
                "exhibit": "Экспонат",
                "master": "Автор"
            }.get(result["type"], result["type"].capitalize())

            # Создаем и размещаем кнопку
            btn = ttk.Button(
                results_frame,
                text=f"{type_text}: {result['name']}",
                command=make_handler(result),
                width=60
            )

            # Назначаем обработчик в зависимости от типа результата
            if result["type"] == "exhibition":
                btn.configure(command=lambda r=result: show_exhibition_and_highlight(r["id"]))
            elif result["type"] == "master":
                btn.configure(command=lambda r=result: show_author_and_highlight(r["id"]))
            elif result["type"] == "exhibit":
                btn.configure(command=lambda r=result: show_exhibit_details(r["id"]))

            btn.pack(pady=5, fill="x")

    else:
        tk.Label(
            results_frame,
            text="Нет результатов",
            font=("Arial", 12)
        ).pack(pady=20)

    # Обновляем геометрию
    def update_scrollregion():
        try:
            canvas.update_idletasks()
            bbox = canvas.bbox("all")
            if bbox:  # Проверяем, что есть элементы для отображения
                canvas.config(scrollregion=bbox)
                # Центрируем содержимое только если оно меньше canvas
                canvas_width = canvas.winfo_width()
                frame_width = results_frame.winfo_reqwidth()
                if frame_width < canvas_width:
                    canvas.coords(results_frame, (canvas_width - frame_width) // 2, 0)
        except Exception as e:
            print(f"Ошибка при обновлении scrollregion: {e}")

    canvas.after(100, update_scrollregion)


def show_exhibition_and_highlight(exhibition_id):
    """Показывает список выставок и выделяет нужную"""
    show_exhibitions()  # Переходим в окно выставок

    # Находим индекс выставки в отсортированном списке
    for i, exhibition in enumerate(exhibitions_data):
        if exhibition[0] == exhibition_id:
            # Получаем доступ к listbox через дочерние виджеты content_frame
            for widget in content_frame.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Listbox):
                            child.selection_clear(0, tk.END)
                            child.selection_set(i)
                            child.see(i)
                            child.activate(i)

                            # Вызываем обработчик выбора, чтобы показать информацию
                            child.event_generate("<<ListboxSelect>>")
                            break
                    break
            break


def show_exhibit_details(exhibit_id):
    """Отображает подробную информацию об экспонате."""
    clear_content()
    # (Здесь код для отображения информации об экспонате)
    print(f"Отображаем информацию об экспонате с ID: {exhibit_id}")
    for exhibit in exhibits_DATA:
        if exhibit[1] == exhibit_id:
            name_label = tk.Label(content_frame, text = exhibit[2], font = ('Arial', 12))
            name_label.pack()


def show_author_and_highlight(master_id):
    """Показывает список авторов и выделяет нужного"""
    show_authors(highlight_id=master_id)  # Передаем ID для выделения

    # Дополнительная прокрутка через 100мс
    content_frame.after(100, lambda: scroll_to_author(master_id))


def scroll_to_author(master_id):
    """Прокручивает к нужному автору"""
    for widget in content_frame.winfo_children():
        if isinstance(widget, ttk.PanedWindow):
            for paned in widget.winfo_children():
                if isinstance(paned, tk.Frame):
                    for container in paned.winfo_children():
                        if isinstance(container, tk.Frame):
                            for canvas in container.winfo_children():
                                if isinstance(canvas, tk.Canvas):
                                    scrollable_frame = canvas.winfo_children()[0]
                                    for author_frame in scrollable_frame.winfo_children():
                                        if hasattr(author_frame, 'author_id') and str(author_frame.author_id) == str(master_id):
                                            # Прокручиваем к автору
                                            canvas.yview_moveto(
                                                max(0, min(1, author_frame.winfo_y() / scrollable_frame.winfo_height())))
                                            return


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

    # Чтение данных из exhibitions.csv

    # Сортировка выставок по дате начала (от новых к старым)
    try:
        exhibitions_data.sort(key=lambda x: datetime.datetime.strptime(x[2], "%Y-%m-%d"), reverse=True)
    except (ValueError, IndexError) as e:
        tk.messagebox.showerror("Ошибка", f"Ошибка при сортировке выставок: {e}. Проверьте формат дат в файле.")

    # Чтение данных из location.csv

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


def show_authors(highlight_id=None):
    clear_content()

    # Создаем основной контейнер с разделением на две части
    paned_window = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
    paned_window.pack(fill=tk.BOTH, expand=True)

    # Левая панель для списка авторов
    left_frame = ttk.Frame(paned_window, width=500)

    # Правая панель для детальной информации (изначально пустая)
    right_frame = ttk.Frame(paned_window, width=400)
    info_label = tk.Label(right_frame, text="Выберите автора для просмотра информации",
                          font=('Arial', 14, 'bold'), wraplength=450, justify='left')
    info_label.pack(padx=20, pady=35)

    paned_window.add(left_frame)
    paned_window.add(right_frame)

    # Кнопка "Назад" в левом верхнем углу
    back_button = ttk.Button(left_frame, text="< Назад", command=show_main_menu)
    back_button.pack(anchor="nw", padx=5, pady=5)

    # Заголовок списка авторов
    label = tk.Label(left_frame, text="Список авторов:", font=('Arial', 14, 'bold'))
    label.pack(pady=(0, 15))

    # Фрейм для списка с прокруткой
    list_container = tk.Frame(left_frame)
    list_container.pack(fill="both", expand=True)

    # Создаем canvas и скроллбар
    canvas = tk.Canvas(list_container)
    scrollbar = tk.Scrollbar(
        list_container,
        orient="vertical",
        command=canvas.yview,
        width=15
    )
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Загрузка данных из CSV файла
    def load_authors():
        authors = []
        try:
            with open('masters.csv', mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file, delimiter=';')
                for row in reader:
                    authors.append({
                        'id': row['ID_master'],
                        'name': row['name'],
                        'years': row['year_of_live'],
                        'city': row['city'],
                        'country': row['country']
                    })
        except FileNotFoundError:
            print("Файл masters.csv не найден")
        return authors

    # Получаем список авторов
    authors = load_authors()

    # Функция для отображения информации об авторе в правой панели
    def show_author_info(author):
        # Очищаем правую панель
        for widget in right_frame.winfo_children():
            widget.destroy()

        # Основная информация
        info_frame = tk.Frame(right_frame)
        info_frame.pack(fill="both", expand=True, padx=20, pady=35)

        name_label = tk.Label(info_frame, text=author["name"], font=('Arial', 16, 'bold'))
        name_label.pack(pady=(0, 15))

        details = [
            f"Годы жизни: {author['years']}",
            f"Место рождения: {author['city']}, {author['country']}"
        ]

        for detail in details:
            tk.Label(info_frame, text=detail, font=('Arial', 12), justify='left').pack(anchor='w', pady=2)

    # Создаем кнопки для каждого автора
    for author in authors:
        # Используем Label вместо Button для лучшего отображения
        frame = tk.Frame(scrollable_frame)
        frame.pack(fill="x", pady=2)

        frame.author_id = author['id']  # Сохраняем ID автора во frame

        # Если это автор для выделения - сразу отмечаем
        if highlight_id and str(author['id']) == str(highlight_id):
            bg_color = '#a0d0ff'
            relief = 'sunken'
        else:
            bg_color = '#f0f0f0'
            relief = 'ridge'

        # Стиль для "кнопки"
        lbl = tk.Label(
            frame,
            text=author['name'],
            font=('Arial', 11),
            anchor='w',
            padx=10,
            pady=5,
            bg=bg_color,
            relief=relief
        )
        lbl.pack(fill="x")

        # Делаем кликабельным
        lbl.bind("<Button-1>", lambda e, a=author: show_author_info(a))
        lbl.bind("<Enter>", lambda e: e.widget.config(bg='#e0e0e0'))
        lbl.bind("<Leave>", lambda e: e.widget.config(bg='#f0f0f0'))

        # Автоматически подбираем ширину
        max_width = max(
            tkFont.Font(family='Arial', size=11).measure(author['name'])  # Use tkFont.Font
            for author in authors) + 30  # Добавляем отступы

        canvas.config(width=min(max_width, 500))  # Ограничиваем максимальную ширину



def create_window():
    """Создает пустое окно размером с четверть экрана."""
    global root, content_frame, search_entry, search_button

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

    # Frame для поисковой строки и кнопки с увеличенными отступами
    search_frame = tk.Frame(root, bg="#ADD8E6")
    search_frame.pack(pady=(window_height // 16, 0), padx=20)  # Добавлен padx=20 для отступов слева/справа

    # Поисковая строка с фиксированной шириной
    search_entry = ttk.Entry(search_frame, width=50)
    search_entry.pack(side="left", padx=(10, 5), pady=5)  # Левый отступ 10, правый 5

    # Кнопка поиска сразу справа
    search_button = ttk.Button(search_frame, text="Искать", command=search)
    search_button.pack(side="left", pady=5, padx=(0, 10))  # Правый отступ 10

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

    # def show_main_menu():

    # def show_exhibitions():

    # def show_exhibits_for_exhibition(exhibition_id, exhibition_name):


    load_data()
    show_main_menu()

root = tk.Tk() # Создаем главное окно Tkinter
create_window() # Вызываем функцию для создания окна
root.mainloop() # Запускаем главный цикл обработки событий (окно будет отображаться, пока программа работает)

