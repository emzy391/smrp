import csv
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


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
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        label = tk.Label(content_frame, text="Информация о выставках будет здесь.", font=('Arial', 12))
        label.pack(pady=20)
        # Здесь должен быть код для отображения информации о выставках

    def show_exhibits():
        clear_content()
        back_button = ttk.Button(content_frame, text="< Назад", command=show_main_menu)
        back_button.pack(anchor="nw", padx=5, pady=5)

        label = tk.Label(content_frame, text="Информация об экспонатах будет здесь.", font=('Arial', 12))
        label.pack(pady=20)
        # Здесь должен быть код для отображения информации об экспонатах

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

    # Отображаем основное меню при запуске
    show_main_menu()


root = tk.Tk() # Создаем главное окно Tkinter
create_window() # Вызываем функцию для создания окна
root.mainloop() # Запускаем главный цикл обработки событий (окно будет отображаться, пока программа работает)

