import csv
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import time
from tkinter import messagebox


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

        # Создаем основной контейнер первым
        main_container = tk.Frame(content_frame)
        main_container.pack(fill="both", expand=True)

        # Затем создаем верхний фрейм для основных кнопок
        frame_buttons = tk.Frame(main_container)
        frame_buttons.pack(pady=(0, 20))

        # Стиль для кнопок
        style_button = ttk.Style()
        style_button.configure("My.TButton",
                               font=('Arial', 14),
                               padding=10)

        # Основные кнопки меню
        button_exhibitions = ttk.Button(frame_buttons, text="Выставки", style="My.TButton", width=20,
                                        command=show_exhibitions)
        button_exhibits = ttk.Button(frame_buttons, text="Экспонаты", style="My.TButton", width=20,
                                     command=show_exhibits)
        button_authors = ttk.Button(frame_buttons, text="Авторы", style="My.TButton", width=20,
                                    command=show_authors)

        button_exhibitions.pack(pady=5)
        button_exhibits.pack(pady=5)
        button_authors.pack(pady=5)

        # Пустое пространство для выравнивания
        spacer = tk.Frame(main_container, height=20)
        spacer.pack(fill="x")

        # Центральный фрейм для кнопок редактирования
        frame_edit_buttons = tk.Frame(main_container)
        frame_edit_buttons.pack(pady=20)  # Отступы сверху и снизу

        # Кнопки добавления и удаления
        button_add = ttk.Button(frame_edit_buttons, text="Добавить", style="My.TButton", width=15,
                                command=add_item)

        button_add.pack(side="left", padx=10)

        # Нижний заполнитель для центрирования
        bottom_spacer = tk.Frame(main_container)
        bottom_spacer.pack(fill="both", expand=True)

    def add_author():
        """Функция для добавления нового автора"""
        author_window = tk.Toplevel(root)
        author_window.title("Добавить автора")
        author_window.geometry("300x200")
        show_add_author_form()

    def add_exhibition():
        exhibition_window = tk.Toplevel(root)
        exhibition_window.title("Добавить автора")
        exhibition_window.geometry("300x200")
        show_add_exhibition_form()

    def add_exhibit():
        exhibit_window = tk.Toplevel(root)
        exhibit_window.title("Добавить автора")
        exhibit_window.geometry("300x200")
        show_add_exhibit_form()

    def add_item():
        """Функция для добавления нового элемента"""
        add_window = tk.Toplevel(root)
        add_window.title("Добавить элемент")
        add_window.geometry("300x200")

        # Центрирование окна
        window_width = 300
        window_height = 200
        screen_width = add_window.winfo_screenwidth()
        screen_height = add_window.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        label = tk.Label(add_window, text="Выберите что добавить:", font=('Arial', 12))
        label.pack(pady=10)

        # Кнопки выбора типа элемента
        btn_frame = tk.Frame(add_window)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Выставку", width=15, command=add_exhibition).pack(pady=5)
        tk.Button(btn_frame, text="Экспонат", width=15, command=add_exhibit).pack(pady=5)
        tk.Button(btn_frame, text="Автора", width=15, command=add_author).pack(pady=5)

    def show_add_exhibition_form():
        """Форма для добавления новой выставки с выбором локации"""
        form_window = tk.Toplevel(root)
        form_window.title("Добавить выставку")
        form_window.geometry("500x500")

        # Переменные для хранения данных
        name_var = tk.StringVar()
        start_date_var = tk.StringVar()
        end_date_var = tk.StringVar()
        location_id_var = tk.StringVar()
        location_info_var = tk.StringVar(value="Не выбрано")

        # Функция загрузки локаций из файла
        def load_locations():
            locations = []
            try:
                with open('location.csv', 'r', encoding='utf-8') as file:
                    reader = csv.reader(file, delimiter=';')
                    next(reader)  # Пропускаем заголовок
                    for row in reader:
                        if len(row) >= 5:
                            locations.append({
                                'id': row[0],
                                'city': row[1],
                                'address': row[2],
                                'organization': row[3],
                                'phone': row[4],
                                'display': f"{row[3]} ({row[1]}, {row[2]})"
                            })
            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл с локациями не найден")
            return locations

        # Функция открытия формы выбора локации
        def choose_location():
            locations = load_locations()
            if not locations:
                messagebox.showinfo("Информация", "Нет доступных локаций")
                return

            loc_window = tk.Toplevel(form_window)
            loc_window.title("Выберите локацию")

            # Таблица с локациями
            tree = ttk.Treeview(loc_window, columns=('id', 'city', 'address', 'org', 'phone'), show='headings')
            tree.heading('id', text='ID')
            tree.heading('city', text='Город')
            tree.heading('address', text='Адрес')
            tree.heading('org', text='Организация')
            tree.heading('phone', text='Телефон')

            for loc in locations:
                tree.insert('', 'end',
                            values=(loc['id'], loc['city'], loc['address'], loc['organization'], loc['phone']))

            tree.pack(fill='both', expand=True)

            def on_select():
                selected = tree.focus()
                if selected:
                    values = tree.item(selected, 'values')
                    location_id_var.set(values[0])
                    location_info_var.set(f"{values[3]} ({values[1]}, {values[2]})")
                    loc_window.destroy()

            ttk.Button(loc_window, text="Выбрать", command=on_select).pack(pady=5)

        # Функция добавления новой локации
        def add_new_location():
            """Форма для добавления новой локации"""
            loc_form = tk.Toplevel(form_window)
            loc_form.title("Добавить новую локацию")
            loc_form.geometry("400x300")

            # Переменные для хранения данных
            city_var = tk.StringVar()
            address_var = tk.StringVar()
            org_var = tk.StringVar()
            phone_var = tk.StringVar()

            # Поля формы
            tk.Label(loc_form, text="Город:").pack(pady=5)
            city_entry = tk.Entry(loc_form, width=40, textvariable=city_var)
            city_entry.pack(pady=5)

            tk.Label(loc_form, text="Адрес:").pack(pady=5)
            address_entry = tk.Entry(loc_form, width=40, textvariable=address_var)
            address_entry.pack(pady=5)

            tk.Label(loc_form, text="Организация:").pack(pady=5)
            org_entry = tk.Entry(loc_form, width=40, textvariable=org_var)
            org_entry.pack(pady=5)

            tk.Label(loc_form, text="Телефон:").pack(pady=5)
            phone_entry = tk.Entry(loc_form, width=40, textvariable=phone_var)
            phone_entry.pack(pady=5)

            def save_location():
                # Проверка обязательных полей
                if not all([city_var.get(), address_var.get(), org_var.get()]):
                    messagebox.showerror("Ошибка", "Заполните обязательные поля (Город, Адрес, Организация)")
                    return

                try:
                    # Генерация ID
                    last_id = 0
                    try:
                        with open('location.csv', 'r', encoding='utf-8') as file:
                            reader = csv.reader(file, delimiter=';')
                            next(reader)  # Пропускаем заголовок
                            for row in reader:
                                if row and row[0].isdigit():
                                    current_id = int(row[0])
                                    if current_id > last_id:
                                        last_id = current_id
                    except FileNotFoundError:
                        pass  # Файл не существует, начнем с ID 1

                    new_id = str(last_id + 1)
                    phone = phone_var.get() if phone_var.get() else "null"

                    # Запись новой локации
                    with open('location.csv', 'a', newline='', encoding='utf-8') as file:
                        writer = csv.writer(file, delimiter=';')
                        writer.writerow([
                            new_id,
                            city_var.get(),
                            address_var.get(),
                            org_var.get(),
                            phone
                        ])

                    # Обновляем информацию о выбранной локации
                    location_id_var.set(new_id)
                    location_info_var.set(f"{org_var.get()} ({city_var.get()}, {address_var.get()})")

                    messagebox.showinfo("Успех", "Локация успешно добавлена")
                    loc_form.destroy()

                except Exception as e:
                    messagebox.showerror("Ошибка", f"Не удалось добавить локацию: {str(e)}")

            # Кнопки управления
            btn_frame = tk.Frame(loc_form)
            btn_frame.pack(pady=10)

            tk.Button(btn_frame, text="Сохранить", command=save_location).pack(side='left', padx=5)
            tk.Button(btn_frame, text="Отмена", command=loc_form.destroy).pack(side='left', padx=5)

        # Поля формы
        tk.Label(form_window, text="Название выставки:").pack(pady=5)
        name_entry = tk.Entry(form_window, width=50, textvariable=name_var)
        name_entry.pack(pady=5)

        tk.Label(form_window, text="Дата начала (ДД-ММ-ГГГГ):").pack(pady=5)
        start_date_entry = tk.Entry(form_window, width=50, textvariable=start_date_var)
        start_date_entry.pack(pady=5)

        tk.Label(form_window, text="Дата окончания (ДД-ММ-ГГГГ):").pack(pady=5)
        end_date_entry = tk.Entry(form_window, width=50, textvariable=end_date_var)
        end_date_entry.pack(pady=5)

        # Поле для локации
        tk.Label(form_window, text="Место проведения:").pack(pady=5)
        tk.Label(form_window, textvariable=location_info_var, relief='sunken', width=50, anchor='w').pack(pady=5)

        btn_frame = tk.Frame(form_window)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Выбрать локацию", command=choose_location).pack(side='left', padx=5)
        tk.Button(btn_frame, text="Добавить новую", command=add_new_location).pack(side='left', padx=5)

        def save_exhibition():
            # Проверка заполнения полей
            if not all([name_var.get(), start_date_var.get(), end_date_var.get(), location_id_var.get()]):
                messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
                return

            try:
                # Генерация ID выставки
                last_id = 0
                try:
                    with open('exhibitions.csv', 'r', encoding='utf-8') as file:
                        reader = csv.reader(file, delimiter=';')
                        for row in reader:
                            if row and row[0].isdigit():
                                current_id = int(row[0])
                                if current_id > last_id:
                                    last_id = current_id
                except FileNotFoundError:
                    pass

                new_exhibition_id = str(last_id + 1)

                # Запись в CSV
                with open('exhibitions.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([
                        new_exhibition_id,
                        name_var.get(),
                        start_date_var.get(),
                        end_date_var.get(),
                        location_id_var.get()  # Сохраняем ID локации
                    ])

                messagebox.showinfo("Успех", "Выставка успешно добавлена")
                form_window.destroy()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

        tk.Button(form_window, text="Сохранить", command=save_exhibition).pack(pady=15)

    def show_add_exhibit_form():
        """Форма для добавления нового экспоната с проверкой автора"""
        form_window = tk.Toplevel(root)
        form_window.title("Добавить экспонат")
        form_window.geometry("650x650")

        # Переменные для хранения данных
        name_var = tk.StringVar()
        year_var = tk.StringVar()
        type_var = tk.StringVar()
        genre_var = tk.StringVar()
        materials_var = tk.StringVar()
        author_name_var = tk.StringVar()
        author_id_var = tk.StringVar()  # Добавлено для хранения ID автора

        # Фрейм для основной информации об экспонате
        exhibit_frame = ttk.LabelFrame(form_window, text="Информация об экспонате", padding=10)
        exhibit_frame.pack(fill="x", padx=10, pady=5)

        # Поля формы экспоната
        ttk.Label(exhibit_frame, text="Название экспоната:").pack(pady=5)
        ttk.Entry(exhibit_frame, width=50, textvariable=name_var).pack(pady=5)

        ttk.Label(exhibit_frame, text="Год создания:").pack(pady=5)
        ttk.Entry(exhibit_frame, width=50, textvariable=year_var).pack(pady=5)

        ttk.Label(exhibit_frame, text="Тип экспоната:").pack(pady=5)
        ttk.Entry(exhibit_frame, width=47, textvariable=type_var).pack(pady=5)

        ttk.Label(exhibit_frame, text="Жанр/Техника:").pack(pady=5)
        ttk.Entry(exhibit_frame, width=50, textvariable=genre_var).pack(pady=5)

        ttk.Label(exhibit_frame, text="Материалы (через запятую):").pack(pady=5)
        ttk.Entry(exhibit_frame, width=50, textvariable=materials_var).pack(pady=5)

        # Фрейм для информации об авторе
        author_frame = ttk.LabelFrame(form_window, text="Информация об авторе", padding=10)
        author_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(author_frame, text="ФИО автора:").pack(pady=5)
        author_entry = ttk.Entry(author_frame, width=50, textvariable=author_name_var)
        author_entry.pack(pady=5)

        ttk.Label(author_frame, text="ID автора:").pack(pady=5)
        ttk.Entry(author_frame, width=50, textvariable=author_id_var, state='readonly').pack(pady=5)

        # Функция для проверки и добавления автора
        def check_and_add_author():
            author_name = author_name_var.get().strip()
            if not author_name:
                messagebox.showerror("Ошибка", "Введите ФИО автора")
                return

            try:
                # Проверяем существование автора
                with open('masters.csv', 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        if row['name'].lower() == author_name.lower():
                            author_id_var.set(row['ID_master'])
                            messagebox.showinfo("Автор найден", f"Автор найден в базе. ID: {row['ID_master']}")
                            return

                # Если автор не найден - предлагаем добавить
                if messagebox.askyesno("Автор не найден", "Добавить нового автора?"):
                    form_window.withdraw()  # Скрываем текущую форму
                    show_add_author_form(author_name, form_window, author_id_var)

            except FileNotFoundError:
                messagebox.showerror("Ошибка", "Файл с авторами не найден")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при поиске автора: {str(e)}")

        # Функция сохранения экспоната
        def save_exhibit():
            # Проверка заполнения всех полей
            if not all([name_var.get(), year_var.get(), type_var.get(),
                        genre_var.get(), materials_var.get(), author_name_var.get()]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            # Проверка существования автора
            if not author_id_var.get():
                messagebox.showerror("Ошибка", "Проверьте автора перед сохранением")
                return

            try:
                material_names = [m.strip() for m in materials_var.get().split(',')]
                material_ids = []

                # Читаем существующие материалы
                existing_materials = {}
                try:
                    with open('materials.csv', 'r', encoding='utf-8') as file:
                        reader = csv.reader(file, delimiter=';')
                        for row in reader:
                            if len(row) >= 2:
                                existing_materials[row[1].lower()] = row[0]
                except FileNotFoundError:
                    pass  # Файл не существует, создадим новый

                # Для каждого материала проверяем наличие
                for material in material_names:
                    if not material:
                        continue

                    if material.lower() in existing_materials:
                        # Материал уже есть - используем существующий ID
                        material_ids.append(existing_materials[material.lower()])
                    else:
                        # Материал новый - добавляем в файл
                        last_material_id = 0
                        try:
                            with open('materials.csv', 'r', encoding='utf-8') as file:
                                for line in file:
                                    parts = line.strip().split(';')
                                    if parts and parts[0].isdigit():
                                        current_id = int(parts[0])
                                        if current_id > last_material_id:
                                            last_material_id = current_id
                        except FileNotFoundError:
                            pass

                        new_material_id = str(last_material_id + 1)
                        with open('materials.csv', 'a', newline='', encoding='utf-8') as file:
                            writer = csv.writer(file, delimiter=';')
                            writer.writerow([new_material_id, material])

                        material_ids.append(new_material_id)
                        existing_materials[material.lower()] = new_material_id

                # Получаем последний ID из файла (вторая колонка)
                last_id = 0
                with open('exhibits.csv', 'r', encoding='utf-8') as file:
                    # Читаем все строки файла
                    lines = file.readlines()

                    # Если файл не пустой и есть хотя бы одна строка с данными (помимо заголовка)
                    if len(lines) > 1:
                        # Получаем последнюю строку с данными
                        last_line = lines[-1].strip()
                        if last_line:
                            # Разбиваем по разделителю ;
                            parts = last_line.split(';')
                            if len(parts) > 1:  # Проверяем, что есть вторая колонка
                                try:
                                    last_id = int(parts[1])  # Берем ID из второй колонки
                                except (IndexError, ValueError):
                                    pass

                # Новый ID = последний ID + 1
                new_exhibit_id = str(last_id + 1)

                with open('exhibits.csv', 'a', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow([
                        "null",
                        new_exhibit_id,
                        name_var.get(),
                        year_var.get(),
                        type_var.get(),
                        genre_var.get(),
                        ','.join(material_ids),
                        author_id_var.get()
                    ])
                messagebox.showinfo("Успех", "Экспонат успешно добавлен")
                form_window.destroy()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить экспонат: {str(e)}")

        # Кнопки управления
        button_frame = tk.Frame(form_window)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Сохранить экспонат",
                   command=save_exhibit).pack(side="left", padx=5)

        # Автоматическая проверка при потере фокуса
        def on_author_focusout(event):
            if author_name_var.get().strip() and not author_id_var.get():
                check_and_add_author()

        author_entry.bind("<FocusOut>", on_author_focusout)

    def show_add_author_form(author_name=None, parent_window=None, author_id_var=None):
        """Форма для добавления нового автора"""
        form_window = tk.Toplevel(root)
        form_window.title("Добавить автора")
        form_window.geometry("400x400")

        # Переменные для хранения данных
        name_var = tk.StringVar(value=author_name if author_name else "")
        birth_var = tk.StringVar()
        death_var = tk.StringVar()
        place_var = tk.StringVar()

        # Поля формы
        ttk.Label(form_window, text="ФИО автора:").pack(pady=5)
        name_entry = ttk.Entry(form_window, width=30, textvariable=name_var)
        if author_name:
            name_entry.config(state='readonly')
        name_entry.pack(pady=5)

        ttk.Label(form_window, text="Год рождения:").pack(pady=5)
        ttk.Entry(form_window, width=30, textvariable=birth_var).pack(pady=5)

        ttk.Label(form_window, text="Год смерти (если нет - оставить пустым):").pack(pady=5)
        ttk.Entry(form_window, width=30, textvariable=death_var).pack(pady=5)

        ttk.Label(form_window, text="Место рождения:").pack(pady=5)
        ttk.Entry(form_window, width=30, textvariable=place_var).pack(pady=5)

        def save_author():
            if not all([name_var.get(), birth_var.get(), place_var.get()]):
                messagebox.showerror("Ошибка", "Обязательные поля не заполнены")
                return

            try:
                # Получаем последний ID из файла (первая колонка)
                last_id = 0
                with open('masters.csv', 'r', encoding='utf-8') as file:
                    for line in file:
                        line = line.strip()
                        if line:  # Пропускаем пустые строки
                            parts = line.split(';')
                            if len(parts) > 0:  # Проверяем, что есть первая колонка
                                try:
                                    current_id = int(parts[0])
                                    if current_id > last_id:
                                        last_id = current_id
                                except (IndexError, ValueError):
                                    pass

                # Новый ID = последний ID + 1
                new_id = str(last_id + 1)

                # Формируем строку для записи
                death_year = death_var.get() if death_var.get() else ""
                years = f"{birth_var.get()}-{death_year}" if death_year else birth_var.get()

                new_record = [
                    new_id,  # ID автора (первая колонка)
                    name_var.get(),
                    years,
                    place_var.get()
                ]

                # Запись данных автора
                with open('masters.csv', 'a', newline='', encoding='utf-8') as file:
                    file.write(';'.join(new_record) + '\n')

                # Если форма вызвана из формы экспоната
                if parent_window and author_id_var:
                    author_id_var.set(new_id)
                    parent_window.deiconify()  # Показываем снова форму экспоната

                messagebox.showinfo("Успех", f"Автор '{name_var.get()}' успешно добавлен с ID: {new_id}")
                form_window.destroy()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {str(e)}")

        ttk.Button(form_window, text="Сохранить", command=save_author).pack(pady=15)

        # Обработка закрытия формы (если вызвана из формы экспоната)
        if parent_window:
            def on_closing():
                parent_window.deiconify()
                form_window.destroy()

            form_window.protocol("WM_DELETE_WINDOW", on_closing)

    def show_exhibitions():
        clear_content()
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        label = tk.Label(content_frame, text="Информация о выставках будет здесь.", font=('Arial', 12))
        label.pack(pady=20)
        # Здесь должен быть код для отображения информации о выставках

    def show_exhibits():
        clear_content()

        # Создаем основной контейнер с разделением на две части
        paned_window = ttk.PanedWindow(content_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)

        # Левая панель для списка экспонатов
        left_frame = ttk.Frame(paned_window, width=300)

        # Правая панель для детальной информации (изначально пустая)
        right_frame = ttk.Frame(paned_window, width=550)
        info_label = tk.Label(right_frame, text="Выберите экспонат для просмотра информации",
                              font=('Arial', 14, 'bold'), wraplength=500, justify='left')
        info_label.pack(padx=20, pady=35)

        paned_window.add(left_frame)
        paned_window.add(right_frame)

        # Кнопка "Назад" в левом верхнем углу
        back_button = ttk.Button(left_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        # Заголовок списка экспонатов
        label = tk.Label(left_frame, text="Список экспонатов:", font=('Arial', 14, 'bold'))
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
        def load_exhibits():
            exhibits = []
            try:
                with open('exhibits.csv', mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        exhibits.append({
                            'ID_exhibition': row['ID_exhibition'],
                            'ID_exhibit': row['ID_exhibit'],
                            'name': row['name'],
                            'year_of_creating': row['year_of_creating'],
                            'type_of_exhibit': row['type_of_exhibit'],
                            'genre_technic': row['genre_technic'],
                            'materials': row['materials'],
                            'ID_master': row['ID_master']
                        })
            except FileNotFoundError:
                print("Файл exhibits.csv не найден")
            return exhibits

        def load_materials():
            materials = {}
            try:
                with open('materials.csv', mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        materials[row['ID_material']] = row['material']
            except FileNotFoundError:
                print("Файл materials.csv не найден")
            return materials

        materials_data = load_materials()

        def load_masters():  # Renamed for clarity
            masters = {}
            try:
                with open('masters.csv', mode='r', encoding='utf-8') as file:
                    reader = csv.DictReader(file, delimiter=';')
                    for row in reader:
                        masters[row['ID_master']] = row['name']  # Store ID:Name
            except FileNotFoundError:
                print("Файл masters.csv не найден")
            return masters

        masters_data = load_masters()

        # Получаем список экспонатов
        exhibits = load_exhibits()

        # Функция для отображения информации об экспонате в правой панели
        def show_exhibit_info(exhibit):
            # Очищаем правую панель
            for widget in right_frame.winfo_children():
                widget.destroy()

            # Основная информация
            info_frame = tk.Frame(right_frame)
            info_frame.pack(fill="both", expand=True, padx=20, pady=35)

            name_label = tk.Label(info_frame, text=exhibit["name"], font=('Arial', 14, 'bold'))
            name_label.pack(pady=(0, 15))

            # Replace material IDs with names
            material_ids = exhibit['materials'].split(',') if exhibit[
                'materials'] else []  # Handle potential empty or missing values
            material_names = [materials_data.get(material_id, "Неизвестно") for material_id in material_ids]
            materials_string = ", ".join(material_names)

            # Display master name instead of ID
            master_id = exhibit['ID_master']
            master_name = masters_data.get(master_id, "Неизвестно")  # Look up the name
            details = [
                f"Автор: {master_name}",  # Display the name
                f"Год создания: {exhibit['year_of_creating']}",
                f"Тип: {exhibit['type_of_exhibit']}",
                f"Жанр/Техника: {exhibit['genre_technic']}",
                f"Материалы: {materials_string}",
            ]

            for detail in details:
                tk.Label(info_frame, text=detail, font=('Arial', 12), justify='left').pack(anchor='w', pady=2)

        # Создаем кнопки для каждого экспоната
        for exhibit in exhibits:
            # Используем Label вместо Button для лучшего отображения
            frame = tk.Frame(scrollable_frame)
            frame.pack(fill="x", pady=2)

            # Стиль для "кнопки"
            lbl = tk.Label(
                frame,
                text=exhibit['name'],
                font=('Arial', 10),
                anchor='w',
                padx=10,
                pady=5,
                bg='#f0f0f0',
                relief='ridge'
            )
            lbl.pack(fill="x")

            # Делаем кликабельным
            lbl.bind("<Button-1>", lambda e, a=exhibit: show_exhibit_info(a))
            lbl.bind("<Enter>", lambda e: e.widget.config(bg='#e0e0e0'))
            lbl.bind("<Leave>", lambda e: e.widget.config(bg='#f0f0f0'))

            # Автоматически подбираем ширину
            max_width = max(
                tkFont.Font(family='Arial', size=10).measure(exhibit['name'])
                for exhibit in exhibits) + 30  # Добавляем отступы

            canvas.config(width=min(max_width, 500))  # Ограничиваем максимальную ширину

    def show_authors():
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

            name_label = tk.Label(info_frame, text=author["name"], font=('Arial', 14, 'bold'))
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

            # Стиль для "кнопки"
            lbl = tk.Label(
                frame,
                text=author['name'],
                font=('Arial', 11),
                anchor='w',
                padx=10,
                pady=5,
                bg='#f0f0f0',
                relief='ridge'
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

    # Отображаем основное меню при запуске
    show_main_menu()


root = tk.Tk() # Создаем главное окно Tkinter
create_window() # Вызываем функцию для создания окна
root.mainloop() # Запускаем главный цикл обработки событий (окно будет отображаться, пока программа работает)

