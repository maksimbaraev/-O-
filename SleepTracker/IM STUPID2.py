import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np


class SleepTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("😴 Sleep Tracker - Трекер сна")
        self.root.geometry("1200x800")
        self.root.configure(bg="#1a1a2e")

        # Инициализация данных
        self.sleep_data = []
        self.load_data()

        # Стили
        self.setup_styles()

        # Создание интерфейса
        self.create_widgets()

        # Обновление статистики
        self.update_statistics()

    def setup_styles(self):
        """Настройка стилей приложения"""
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Цветовая схема
        self.colors = {
            'bg_dark': '#1a1a2e',
            'bg_medium': '#16213e',
            'bg_light': '#0f3460',
            'accent': '#e94560',
            'text': '#ffffff',
            'success': '#4CAF50',
            'warning': '#FF9800'
        }

        self.style.configure('Dark.TFrame', background=self.colors['bg_dark'])
        self.style.configure('Medium.TFrame', background=self.colors['bg_medium'])
        self.style.configure('Light.TFrame', background=self.colors['bg_light'])

        self.style.configure('Title.TLabel',
                             font=('Arial', 18, 'bold'),
                             background=self.colors['bg_dark'],
                             foreground=self.colors['text'])

        self.style.configure('Card.TFrame',
                             background=self.colors['bg_medium'],
                             relief='solid',
                             borderwidth=1)

        self.style.configure('Stats.TLabel',
                             font=('Arial', 10),
                             background=self.colors['bg_medium'],
                             foreground=self.colors['text'])

        self.style.configure('Accent.TButton',
                             font=('Arial', 10, 'bold'),
                             background=self.colors['accent'],
                             foreground=self.colors['text'])

        self.style.map('Accent.TButton',
                       background=[('active', '#d43d57')])

    def load_data(self):
        """Загрузка данных из файла"""
        if os.path.exists("sleep_data.json"):
            try:
                with open("sleep_data.json", "r", encoding="utf-8") as f:
                    self.sleep_data = json.load(f)
            except:
                self.sleep_data = []
        else:
            self.sleep_data = []

        # Конвертация строк дат в объекты datetime для работы
        for record in self.sleep_data:
            record['date'] = datetime.strptime(record['date'], '%Y-%m-%d').date()

    def save_data(self):
        """Сохранение данных в файл"""
        # Конвертация дат обратно в строки для JSON
        save_data = []
        for record in self.sleep_data:
            record_copy = record.copy()
            record_copy['date'] = record['date'].strftime('%Y-%m-%d')
            save_data.append(record_copy)

        with open("sleep_data.json", "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """Создание интерфейса приложения"""
        # Основной контейнер
        main_container = ttk.Frame(self.root, style='Dark.TFrame', padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        title_frame = ttk.Frame(main_container, style='Dark.TFrame')
        title_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))

        title_label = ttk.Label(title_frame,
                                text="😴 Трекер сна - Анализ и улучшение качества сна",
                                style='Title.TLabel')
        title_label.pack()

        # Основное содержимое - 3 колонки
        content_frame = ttk.Frame(main_container, style='Dark.TFrame')
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Левая колонка - добавление записи и календарь
        left_frame = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Правая колонка - статистика
        right_frame = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Средняя колонка - графики
        middle_frame = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        middle_frame.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.columnconfigure(2, weight=2)
        content_frame.rowconfigure(0, weight=1)
        left_frame.rowconfigure(7, weight=1)
        middle_frame.rowconfigure(1, weight=1)

        # === ЛЕВАЯ КОЛОНКА: Добавление записи и календарь ===
        left_title = ttk.Label(left_frame, text="➕ Добавить запись о сне",
                               font=('Arial', 12, 'bold'),
                               background=self.colors['bg_medium'],
                               foreground=self.colors['text'])
        left_title.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Дата
        ttk.Label(left_frame, text="Дата:",
                  background=self.colors['bg_medium'],
                  foreground=self.colors['text']).grid(row=1, column=0, sticky=tk.W, pady=5)

        self.date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(left_frame, textvariable=self.date_var, width=15)
        date_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Кнопка выбора даты
        date_button = ttk.Button(left_frame, text="📅", width=3,
                                 command=self.show_calendar)
        date_button.grid(row=1, column=1, sticky=tk.E, pady=5)

        # Время отхода ко сну
        ttk.Label(left_frame, text="Время отхода ко сну:",
                  background=self.colors['bg_medium'],
                  foreground=self.colors['text']).grid(row=2, column=0, sticky=tk.W, pady=5)

        self.bedtime_var = tk.StringVar(value="22:30")
        bedtime_entry = ttk.Entry(left_frame, textvariable=self.bedtime_var, width=15)
        bedtime_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Время пробуждения
        ttk.Label(left_frame, text="Время пробуждения:",
                  background=self.colors['bg_medium'],
                  foreground=self.colors['text']).grid(row=3, column=0, sticky=tk.W, pady=5)

        self.wakeup_var = tk.StringVar(value="07:00")
        wakeup_entry = ttk.Entry(left_frame, textvariable=self.wakeup_var, width=15)
        wakeup_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Качество сна
        ttk.Label(left_frame, text="Качество сна (1-10):",
                  background=self.colors['bg_medium'],
                  foreground=self.colors['text']).grid(row=4, column=0, sticky=tk.W, pady=5)

        self.quality_var = tk.IntVar(value=7)
        quality_scale = ttk.Scale(left_frame, from_=1, to=10,
                                  variable=self.quality_var, orient=tk.HORIZONTAL, length=150)
        quality_scale.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        quality_label = ttk.Label(left_frame, textvariable=tk.StringVar(value="7"),
                                  background=self.colors['bg_medium'],
                                  foreground=self.colors['accent'])
        quality_label.grid(row=4, column=1, sticky=tk.E, pady=5)

        # Обновление метки качества
        def update_quality_label(val):
            quality_label.config(text=str(int(float(val))))

        quality_scale.configure(command=update_quality_label)

        # Комментарии
        ttk.Label(left_frame, text="Комментарии:",
                  background=self.colors['bg_medium'],
                  foreground=self.colors['text']).grid(row=5, column=0, sticky=tk.NW, pady=5)

        self.comments_text = tk.Text(left_frame, height=4, width=20,
                                     bg=self.colors['bg_light'], fg=self.colors['text'],
                                     insertbackground=self.colors['text'])
        self.comments_text.grid(row=5, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Кнопка добавления записи
        add_button = ttk.Button(left_frame, text="💾 Сохранить запись",
                                style='Accent.TButton',
                                command=self.add_sleep_record)
        add_button.grid(row=6, column=0, columnspan=2, pady=15)

        # Разделитель
        separator = ttk.Separator(left_frame, orient='horizontal')
        separator.grid(row=7, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=20)

        # История записей
        history_title = ttk.Label(left_frame, text="📋 Последние записи",
                                  font=('Arial', 12, 'bold'),
                                  background=self.colors['bg_medium'],
                                  foreground=self.colors['text'])
        history_title.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Таблица истории
        columns = ("date", "duration", "quality")
        self.history_tree = ttk.Treeview(left_frame, columns=columns,
                                         show="headings", height=8)

        self.history_tree.heading("date", text="Дата")
        self.history_tree.heading("duration", text="Длительность")
        self.history_tree.heading("quality", text="Качество")

        self.history_tree.column("date", width=80)
        self.history_tree.column("duration", width=80)
        self.history_tree.column("quality", width=60)

        # Стилизация таблицы
        self.style.configure("Treeview",
                             background=self.colors['bg_light'],
                             foreground=self.colors['text'],
                             fieldbackground=self.colors['bg_light'],
                             rowheight=25)

        self.style.configure("Treeview.Heading",
                             background=self.colors['accent'],
                             foreground=self.colors['text'],
                             font=('Arial', 9, 'bold'))

        # Скроллбар для таблицы
        tree_scrollbar = ttk.Scrollbar(left_frame, orient="vertical",
                                       command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.history_tree.grid(row=9, column=0, columnspan=2,
                               sticky=(tk.W, tk.E, tk.N, tk.S))
        tree_scrollbar.grid(row=9, column=2, sticky=(tk.N, tk.S))

        # Кнопка удаления записи
        delete_button = ttk.Button(left_frame, text="🗑️ Удалить выбранное",
                                   command=self.delete_selected_record)
        delete_button.grid(row=10, column=0, columnspan=2, pady=(10, 0))

        # === СРЕДНЯЯ КОЛОНКА: Графики ===
        middle_title = ttk.Label(middle_frame, text="📈 Графики сна",
                                 font=('Arial', 12, 'bold'),
                                 background=self.colors['bg_medium'],
                                 foreground=self.colors['text'])
        middle_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))

        # Фрейм для графиков
        self.graph_frame = ttk.Frame(middle_frame, style='Light.TFrame')
        self.graph_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Кнопки управления графиками
        graph_buttons_frame = ttk.Frame(middle_frame, style='Card.TFrame')
        graph_buttons_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Button(graph_buttons_frame, text="Длительность сна",
                   command=lambda: self.plot_sleep_duration()).pack(side=tk.LEFT, padx=2)
        ttk.Button(graph_buttons_frame, text="Качество сна",
                   command=lambda: self.plot_sleep_quality()).pack(side=tk.LEFT, padx=2)
        ttk.Button(graph_buttons_frame, text="Время отхода ко сну",
                   command=lambda: self.plot_bedtime()).pack(side=tk.LEFT, padx=2)
        ttk.Button(graph_buttons_frame, text="Все данные",
                   command=lambda: self.plot_all_data()).pack(side=tk.LEFT, padx=2)

        # === ПРАВАЯ КОЛОНКА: Статистика ===
        right_title = ttk.Label(right_frame, text="📊 Статистика сна",
                                font=('Arial', 12, 'bold'),
                                background=self.colors['bg_medium'],
                                foreground=self.colors['text'])
        right_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))

        # Фрейм для статистики
        stats_container = ttk.Frame(right_frame, style='Light.TFrame', padding="10")
        stats_container.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Статистические метки
        self.stats_labels = {}

        stats_items = [
            ("Всего записей:", "total_records"),
            ("Средняя длительность:", "avg_duration"),
            ("Лучшее качество:", "best_quality"),
            ("Худшее качество:", "worst_quality"),
            ("Рекомендуемая норма:", "recommended"),
            ("Соответствие норме:", "norm_compliance"),
            ("Среднее время отхода:", "avg_bedtime"),
            ("Среднее время подъема:", "avg_wakeup")
        ]

        for i, (label_text, key) in enumerate(stats_items):
            label = ttk.Label(stats_container, text=label_text,
                              style='Stats.TLabel')
            label.grid(row=i, column=0, sticky=tk.W, pady=5)

            value_label = ttk.Label(stats_container, text="0",
                                    style='Stats.TLabel',
                                    font=('Arial', 10, 'bold'),
                                    foreground=self.colors['accent'])
            value_label.grid(row=i, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            self.stats_labels[key] = value_label

        # Разделитель
        separator2 = ttk.Separator(stats_container, orient='horizontal')
        separator2.grid(row=len(stats_items), column=0, columnspan=2,
                        sticky=(tk.W, tk.E), pady=20)

        # Анализ и рекомендации
        analysis_title = ttk.Label(stats_container, text="💡 Рекомендации",
                                   font=('Arial', 11, 'bold'),
                                   background=self.colors['bg_light'],
                                   foreground=self.colors['text'])
        analysis_title.grid(row=len(stats_items) + 1, column=0, columnspan=2,
                            sticky=tk.W, pady=(0, 10))

        self.recommendations_text = tk.Text(stats_container, height=8, width=30,
                                            bg=self.colors['bg_light'],
                                            fg=self.colors['text'],
                                            wrap=tk.WORD,
                                            font=('Arial', 9),
                                            relief='flat')
        self.recommendations_text.grid(row=len(stats_items) + 2, column=0, columnspan=2,
                                       sticky=(tk.W, tk.E, tk.N, tk.S))

        # Кнопка экспорта
        export_button = ttk.Button(right_frame, text="📤 Экспорт данных",
                                   style='Accent.TButton',
                                   command=self.export_data)
        export_button.grid(row=2, column=0, pady=(15, 0))

        # Инициализация графиков
        self.plot_sleep_duration()

        # Загрузка истории
        self.load_history()

    def show_calendar(self):
        """Отображение простого календаря"""
        cal_window = tk.Toplevel(self.root)
        cal_window.title("Выберите дату")
        cal_window.geometry("300x300")
        cal_window.configure(bg=self.colors['bg_dark'])

        # Получаем текущую дату из поля ввода
        current_date = self.date_var.get()
        try:
            year, month, day = map(int, current_date.split('-'))
        except:
            today = datetime.now()
            year, month, day = today.year, today.month, today.day

        # Создаем фрейм для календаря
        cal_frame = ttk.Frame(cal_window, style='Card.TFrame', padding="10")
        cal_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Заголовок с месяцем и годом
        month_names = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                       "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]

        header_frame = ttk.Frame(cal_frame, style='Card.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))

        # Кнопки навигации
        def prev_month():
            nonlocal month, year
            month -= 1
            if month < 1:
                month = 12
                year -= 1
            update_calendar()

        def next_month():
            nonlocal month, year
            month += 1
            if month > 12:
                month = 1
                year += 1
            update_calendar()

        prev_btn = ttk.Button(header_frame, text="◀", width=3, command=prev_month)
        prev_btn.pack(side="left", padx=5)

        self.month_year_label = ttk.Label(header_frame,
                                          text=f"{month_names[month - 1]} {year}",
                                          font=('Arial', 12, 'bold'),
                                          background=self.colors['bg_medium'],
                                          foreground=self.colors['text'])
        self.month_year_label.pack(side="left", expand=True)

        next_btn = ttk.Button(header_frame, text="▶", width=3, command=next_month)
        next_btn.pack(side="right", padx=5)

        # Дни недели
        days_frame = ttk.Frame(cal_frame, style='Card.TFrame')
        days_frame.pack(fill="x")

        days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for i, day in enumerate(days):
            label = ttk.Label(days_frame, text=day,
                              font=('Arial', 9, 'bold'),
                              background=self.colors['bg_medium'],
                              foreground=self.colors['accent'])
            label.grid(row=0, column=i, padx=2, pady=2, ipadx=10, ipady=5)

        # Фрейм для дней
        self.days_frame = ttk.Frame(cal_frame, style='Card.TFrame')
        self.days_frame.pack(fill="both", expand=True)

        def update_calendar():
            """Обновление календаря"""
            # Очищаем предыдущие дни
            for widget in self.days_frame.winfo_children():
                widget.destroy()

            # Обновляем заголовок
            self.month_year_label.config(text=f"{month_names[month - 1]} {year}")

            # Определяем первый день месяца
            first_day = datetime(year, month, 1)
            start_weekday = first_day.weekday()  # 0 = Понедельник, 6 = Воскресенье

            # Определяем количество дней в месяце
            if month == 12:
                next_month = datetime(year + 1, 1, 1)
            else:
                next_month = datetime(year, month + 1, 1)

            days_in_month = (next_month - first_day).days

            # Заполняем календарь
            day_buttons = []

            # Пустые клетки до первого дня
            for i in range(start_weekday):
                empty_label = ttk.Label(self.days_frame, text="",
                                        background=self.colors['bg_medium'])
                empty_label.grid(row=0, column=i, padx=2, pady=2, ipadx=10, ipady=5)

            # Дни месяца
            row, col = 0, start_weekday
            for day in range(1, days_in_month + 1):
                if col >= 7:
                    col = 0
                    row += 1

                day_str = str(day)
                is_today = (day == datetime.now().day and
                            month == datetime.now().month and
                            year == datetime.now().year)

                # Определяем цвет кнопки
                bg_color = self.colors['accent'] if is_today else self.colors['bg_light']
                fg_color = self.colors['text']

                def make_callback(d):
                    return lambda: self.select_date_in_calendar(d, month, year, cal_window)

                day_btn = tk.Button(self.days_frame, text=day_str,
                                    command=make_callback(day),
                                    bg=bg_color, fg=fg_color,
                                    font=('Arial', 9),
                                    relief='flat',
                                    width=3, height=1)
                day_btn.grid(row=row, column=col, padx=2, pady=2)

                day_buttons.append(day_btn)
                col += 1

        def select_date(selected_day):
            """Выбор даты"""
            self.date_var.set(f"{year:04d}-{month:02d}-{selected_day:02d}")
            cal_window.destroy()

        self.select_date_in_calendar = select_date

        # Инициализация календаря
        update_calendar()

        # Кнопка сегодня
        today_btn = ttk.Button(cal_frame, text="Сегодня",
                               command=lambda: self.select_date_in_calendar(
                                   datetime.now().day,
                                   datetime.now().month,
                                   datetime.now().year,
                                   cal_window))
        today_btn.pack(pady=(10, 0))

    def select_date_in_calendar(self, day, month, year, cal_window):
        """Выбор даты в календаре"""
        self.date_var.set(f"{year:04d}-{month:02d}-{day:02d}")
        cal_window.destroy()

    def calculate_duration(self, bedtime, wakeup):
        """Расчет длительности сна"""
        try:
            # Парсинг времени
            bed_h, bed_m = map(int, bedtime.split(':'))
            wake_h, wake_m = map(int, wakeup.split(':'))

            bed_time = timedelta(hours=bed_h, minutes=bed_m)
            wake_time = timedelta(hours=wake_h, minutes=wake_m)

            # Учитываем, что сон может продолжаться после полуночи
            if wake_time < bed_time:
                wake_time += timedelta(days=1)

            duration = wake_time - bed_time
            hours = duration.seconds // 3600
            minutes = (duration.seconds % 3600) // 60

            return f"{hours:02d}:{minutes:02d}", hours + minutes / 60
        except:
            return "00:00", 0

    def add_sleep_record(self):
        """Добавление новой записи о сне"""
        # Проверка данных
        date_str = self.date_var.get()
        bedtime = self.bedtime_var.get()
        wakeup = self.wakeup_var.get()
        quality = self.quality_var.get()
        comments = self.comments_text.get("1.0", tk.END).strip()

        # Валидация даты
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте ГГГГ-ММ-ДД")
            return

        # Валидация времени
        time_format = "%H:%M"
        try:
            datetime.strptime(bedtime, time_format)
            datetime.strptime(wakeup, time_format)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат времени. Используйте ЧЧ:ММ")
            return

        # Проверка, что время пробуждения позже времени отхода
        bed_h, bed_m = map(int, bedtime.split(':'))
        wake_h, wake_m = map(int, wakeup.split(':'))

        bed_minutes = bed_h * 60 + bed_m
        wake_minutes = wake_h * 60 + wake_m

        if wake_minutes <= bed_minutes:
            wake_minutes += 24 * 60  # Добавляем сутки, если пробуждение на следующий день

        duration_minutes = wake_minutes - bed_minutes

        if duration_minutes > 24 * 60:
            messagebox.showerror("Ошибка", "Сон не может длиться более 24 часов")
            return

        # Расчет длительности
        duration_str, duration_hours = self.calculate_duration(bedtime, wakeup)

        # Проверка на дубликаты
        for record in self.sleep_data:
            if record['date'] == date_obj:
                if messagebox.askyesno("Подтверждение",
                                       "Запись на эту дату уже существует. Заменить?"):
                    # Удаляем старую запись
                    self.sleep_data.remove(record)
                    break
                else:
                    return

        # Создание новой записи
        new_record = {
            'date': date_obj,
            'bedtime': bedtime,
            'wakeup': wakeup,
            'duration': duration_str,
            'duration_hours': duration_hours,
            'quality': quality,
            'comments': comments
        }

        # Добавление записи
        self.sleep_data.append(new_record)

        # Сортировка по дате
        self.sleep_data.sort(key=lambda x: x['date'], reverse=True)

        # Сохранение данных
        self.save_data()

        # Обновление интерфейса
        self.load_history()
        self.update_statistics()
        self.plot_sleep_duration()

        # Очистка полей
        self.comments_text.delete("1.0", tk.END)
        messagebox.showinfo("Успех", "Запись успешно добавлена!")

    def load_history(self):
        """Загрузка истории в таблицу"""
        # Очистка таблицы
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)

        # Добавление последних 20 записей
        recent_records = sorted(self.sleep_data, key=lambda x: x['date'], reverse=True)[:20]

        for record in recent_records:
            date_str = record['date'].strftime('%d.%m.%Y')
            quality_str = f"{record['quality']}/10"

            self.history_tree.insert("", tk.END,
                                     values=(date_str, record['duration'], quality_str),
                                     tags=(record['date'].strftime('%Y-%m-%d'),))

    def delete_selected_record(self):
        """Удаление выбранной записи"""
        selection = self.history_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            item = self.history_tree.item(selection[0])
            date_str = item['values'][0]

            # Конвертация даты из формата таблицы
            day, month, year = map(int, date_str.split('.'))
            date_to_delete = datetime(year, month, day).date()

            # Удаление записи
            self.sleep_data = [r for r in self.sleep_data if r['date'] != date_to_delete]

            # Сохранение и обновление
            self.save_data()
            self.load_history()
            self.update_statistics()
            self.plot_sleep_duration()

            messagebox.showinfo("Успех", "Запись удалена")

    def update_statistics(self):
        """Обновление статистики"""
        if not self.sleep_data:
            # Нет данных
            self.stats_labels['total_records'].config(text="0")
            self.stats_labels['avg_duration'].config(text="00:00")
            self.stats_labels['best_quality'].config(text="0/10")
            self.stats_labels['worst_quality'].config(text="0/10")
            self.stats_labels['recommended'].config(text="7-9 часов")
            self.stats_labels['norm_compliance'].config(text="0%")
            self.stats_labels['avg_bedtime'].config(text="--:--")
            self.stats_labels['avg_wakeup'].config(text="--:--")

            self.recommendations_text.delete("1.0", tk.END)
            self.recommendations_text.insert("1.0",
                                             "Добавьте первую запись о сне, чтобы увидеть статистику и рекомендации.")
            return

        # Общие показатели
        total_records = len(self.sleep_data)
        total_duration_hours = sum(r['duration_hours'] for r in self.sleep_data)
        avg_duration_hours = total_duration_hours / total_records

        # Лучшее и худшее качество
        best_quality = max(r['quality'] for r in self.sleep_data)
        worst_quality = min(r['quality'] for r in self.sleep_data)

        # Соответствие норме (7-9 часов)
        recommended_min, recommended_max = 7, 9
        within_norm = sum(1 for r in self.sleep_data
                          if recommended_min <= r['duration_hours'] <= recommended_max)
        norm_compliance = (within_norm / total_records) * 100

        # Среднее время отхода и подъема
        bedtimes = []
        wakeups = []
        for record in self.sleep_data:
            bed_h, bed_m = map(int, record['bedtime'].split(':'))
            wake_h, wake_m = map(int, record['wakeup'].split(':'))

            bed_minutes = bed_h * 60 + bed_m
            wake_minutes = wake_h * 60 + wake_m

            bedtimes.append(bed_minutes)
            wakeups.append(wake_minutes)

        avg_bedtime_min = sum(bedtimes) / len(bedtimes)
        avg_wakeup_min = sum(wakeups) / len(wakeups)

        # Конвертация минут в часы:минуты
        avg_bed_h = int(avg_bedtime_min // 60) % 24
        avg_bed_m = int(avg_bedtime_min % 60)
        avg_wake_h = int(avg_wakeup_min // 60) % 24
        avg_wake_m = int(avg_wakeup_min % 60)

        # Обновление меток
        self.stats_labels['total_records'].config(text=str(total_records))
        self.stats_labels['avg_duration'].config(
            text=f"{int(avg_duration_hours):02d}:{int((avg_duration_hours % 1) * 60):02d}")
        self.stats_labels['best_quality'].config(text=f"{best_quality}/10")
        self.stats_labels['worst_quality'].config(text=f"{worst_quality}/10")
        self.stats_labels['recommended'].config(text="7-9 часов")
        self.stats_labels['norm_compliance'].config(text=f"{norm_compliance:.1f}%")
        self.stats_labels['avg_bedtime'].config(text=f"{avg_bed_h:02d}:{avg_bed_m:02d}")
        self.stats_labels['avg_wakeup'].config(text=f"{avg_wake_h:02d}:{avg_wake_m:02d}")

        # Генерация рекомендаций
        recommendations = self.generate_recommendations(avg_duration_hours,
                                                        norm_compliance,
                                                        avg_bedtime_min,
                                                        avg_wakeup_min,
                                                        best_quality,
                                                        worst_quality)

        self.recommendations_text.delete("1.0", tk.END)
        self.recommendations_text.insert("1.0", recommendations)

    def generate_recommendations(self, avg_duration, norm_compliance,
                                 avg_bedtime, avg_wakeup, best_q, worst_q):
        """Генерация рекомендаций на основе статистики"""
        recommendations = []

        # Рекомендации по длительности
        if avg_duration < 7:
            recommendations.append("⚠️ Ваш средний сон меньше рекомендуемой нормы (7-9 часов).")
            recommendations.append("• Старайтесь ложиться на 30-60 минут раньше")
            recommendations.append("• Избегайте кофеина после 16:00")
        elif avg_duration > 9:
            recommendations.append("⚠️ Ваш средний сон превышает рекомендуемую норму.")
            recommendations.append("• Избыток сна может быть признаком усталости или проблем со здоровьем")
            recommendations.append("• Проконсультируйтесь с врачом, если чувствуете постоянную усталость")
        else:
            recommendations.append("✅ Ваша средняя длительность сна соответствует норме!")

        # Рекомендации по времени отхода
        if avg_bedtime > 23 * 60:  # После 23:00
            recommendations.append("\n🌙 Вы поздно ложитесь спать:")
            recommendations.append("• Старайтесь ложиться до 23:00 для лучшего качества сна")
            recommendations.append("• Создайте вечерний ритуал: чтение, медитация")
        elif avg_bedtime < 22 * 60:  # До 22:00
            recommendations.append("\n🌙 Вы рано ложитесь спать:")
            recommendations.append("• Ранний отход ко сну полезен для здоровья")
            recommendations.append("• Убедитесь, что в комнате темно и тихо")

        # Рекомендации по качеству
        quality_range = best_q - worst_q
        if quality_range > 5:
            recommendations.append(f"\n📊 Качество сна сильно варьируется ({worst_q}-{best_q}/10):")
            recommendations.append("• Старайтесь соблюдать регулярный график")
            recommendations.append("• Отмечайте факторы, влияющие на качество сна")
        elif best_q >= 8:
            recommendations.append("\n🎉 Отличное качество сна!")
            recommendations.append("• Продолжайте в том же духе!")

        # Общие рекомендации
        recommendations.append("\n💡 Общие советы для улучшения сна:")
        recommendations.append("• Поддерживайте регулярный график сна даже в выходные")
        recommendations.append("• Создайте комфортные условия: темно, тихо, прохладно")
        recommendations.append("• Избегайте экранов за 1 час до сна")
        recommendations.append("• Регулярно занимайтесь спортом, но не перед сном")

        return "\n".join(recommendations)

    def plot_sleep_duration(self):
        """Построение графика длительности сна"""
        self.clear_graph_frame()

        if not self.sleep_data:
            no_data_label = ttk.Label(self.graph_frame,
                                      text="Нет данных для отображения\nДобавьте записи о сне",
                                      font=('Arial', 12),
                                      background=self.colors['bg_light'],
                                      foreground=self.colors['text'])
            no_data_label.pack(expand=True)
            return

        # Подготовка данных
        dates = [r['date'] for r in self.sleep_data[-30:]]  # Последние 30 записей
        durations = [r['duration_hours'] for r in self.sleep_data[-30:]]
        qualities = [r['quality'] for r in self.sleep_data[-30:]]

        # Создание фигуры
        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(self.colors['bg_light'])
        ax.set_facecolor(self.colors['bg_light'])

        # График длительности
        bars = ax.bar(range(len(dates)), durations, color=self.colors['accent'], alpha=0.7)

        # Цвет баров в зависимости от качества
        for i, (bar, quality) in enumerate(zip(bars, qualities)):
            if quality >= 8:
                bar.set_color('#4CAF50')  # Зеленый
            elif quality <= 4:
                bar.set_color('#FF5252')  # Красный

        # Линия рекомендуемой нормы
        ax.axhline(y=7, color='yellow', linestyle='--', alpha=0.5, label='Минимум (7ч)')
        ax.axhline(y=9, color='green', linestyle='--', alpha=0.5, label='Максимум (9ч)')

        # Настройки графика
        ax.set_xlabel('Дата', color='white')
        ax.set_ylabel('Длительность сна (часы)', color='white')
        ax.set_title('Длительность сна по дням', color='white', pad=20)

        # Форматирование осей
        ax.tick_params(colors='white')
        ax.spines['bottom'].set_color('white')
        ax.spines['top'].set_color('white')
        ax.spines['left'].set_color('white')
        ax.spines['right'].set_color('white')

        # Отображение только некоторых дат на оси X
        if len(dates) > 10:
            step = len(dates) // 10
            indices = list(range(0, len(dates), step))
            date_labels = [dates[i].strftime('%d.%m') for i in indices]
            ax.set_xticks(indices)
            ax.set_xticklabels(date_labels, rotation=45, ha='right')
        else:
            date_labels = [d.strftime('%d.%m') for d in dates]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(date_labels, rotation=45, ha='right')

        ax.legend(facecolor=self.colors['bg_light'], edgecolor='white',
                  labelcolor='white')

        # Вставка в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_sleep_quality(self):
        """Построение графика качества сна"""
        self.clear_graph_frame()

        if not self.sleep_data:
            return

        dates = [r['date'] for r in self.sleep_data[-30:]]
        qualities = [r['quality'] for r in self.sleep_data[-30:]]

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(self.colors['bg_light'])
        ax.set_facecolor(self.colors['bg_light'])

        # График качества сна
        ax.plot(range(len(dates)), qualities, 'o-', color=self.colors['accent'],
                linewidth=2, markersize=6)

        # Заполнение области под графиком
        ax.fill_between(range(len(dates)), qualities, alpha=0.3, color=self.colors['accent'])

        # Линия среднего качества
        avg_quality = sum(qualities) / len(qualities)
        ax.axhline(y=avg_quality, color='yellow', linestyle='--',
                   alpha=0.7, label=f'Среднее: {avg_quality:.1f}/10')

        ax.set_xlabel('Дата', color='white')
        ax.set_ylabel('Качество сна (1-10)', color='white')
        ax.set_title('Качество сна по дням', color='white', pad=20)
        ax.set_ylim(0, 10.5)

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        if len(dates) > 10:
            step = len(dates) // 10
            indices = list(range(0, len(dates), step))
            date_labels = [dates[i].strftime('%d.%m') for i in indices]
            ax.set_xticks(indices)
            ax.set_xticklabels(date_labels, rotation=45, ha='right')
        else:
            date_labels = [d.strftime('%d.%m') for d in dates]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(date_labels, rotation=45, ha='right')

        ax.legend(facecolor=self.colors['bg_light'], edgecolor='white',
                  labelcolor='white')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_bedtime(self):
        """Построение графика времени отхода ко сну"""
        self.clear_graph_frame()

        if not self.sleep_data:
            return

        dates = [r['date'] for r in self.sleep_data[-30:]]
        bedtimes = []

        for record in self.sleep_data[-30:]:
            h, m = map(int, record['bedtime'].split(':'))
            # Конвертация в десятичные часы
            bedtime_decimal = h + m / 60
            bedtimes.append(bedtime_decimal)

        fig, ax = plt.subplots(figsize=(8, 4))
        fig.patch.set_facecolor(self.colors['bg_light'])
        ax.set_facecolor(self.colors['bg_light'])

        ax.scatter(range(len(dates)), bedtimes, c=bedtimes, cmap='viridis', s=50)

        # Линия тренда
        if len(bedtimes) > 1:
            z = np.polyfit(range(len(dates)), bedtimes, 1)
            p = np.poly1d(z)
            ax.plot(range(len(dates)), p(range(len(dates))), "r--", alpha=0.5)

        ax.set_xlabel('Дата', color='white')
        ax.set_ylabel('Время отхода ко сну', color='white')
        ax.set_title('Время отхода ко сну', color='white', pad=20)

        # Форматирование оси Y как времени
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, pos: f'{int(x):02d}:{int((x % 1) * 60):02d}'))

        ax.tick_params(colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')

        if len(dates) > 10:
            step = len(dates) // 10
            indices = list(range(0, len(dates), step))
            date_labels = [dates[i].strftime('%d.%m') for i in indices]
            ax.set_xticks(indices)
            ax.set_xticklabels(date_labels, rotation=45, ha='right')
        else:
            date_labels = [d.strftime('%d.%m') for d in dates]
            ax.set_xticks(range(len(dates)))
            ax.set_xticklabels(date_labels, rotation=45, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def plot_all_data(self):
        """Построение комплексного графика"""
        self.clear_graph_frame()

        if not self.sleep_data:
            return

        dates = [r['date'] for r in self.sleep_data[-30:]]
        durations = [r['duration_hours'] for r in self.sleep_data[-30:]]
        qualities = [r['quality'] for r in self.sleep_data[-30:]]

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
        fig.patch.set_facecolor(self.colors['bg_light'])
        ax1.set_facecolor(self.colors['bg_light'])
        ax2.set_facecolor(self.colors['bg_light'])

        # График длительности
        bars = ax1.bar(range(len(dates)), durations, color=self.colors['accent'], alpha=0.7)
        ax1.axhline(y=7, color='yellow', linestyle='--', alpha=0.5)
        ax1.axhline(y=9, color='green', linestyle='--', alpha=0.5)
        ax1.set_ylabel('Длительность (ч)', color='white')

        # График качества
        ax2.plot(range(len(dates)), qualities, 'o-', color='#FF9800', linewidth=2)
        ax2.fill_between(range(len(dates)), qualities, alpha=0.3, color='#FF9800')
        ax2.set_ylabel('Качество (1-10)', color='white')
        ax2.set_xlabel('Дата', color='white')
        ax2.set_ylim(0, 10.5)

        # Общие настройки
        for ax in [ax1, ax2]:
            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')

        # Настройки дат на оси X
        if len(dates) > 10:
            step = len(dates) // 10
            indices = list(range(0, len(dates), step))
            date_labels = [dates[i].strftime('%d.%m') for i in indices]
            ax2.set_xticks(indices)
            ax2.set_xticklabels(date_labels, rotation=45, ha='right')
        else:
            date_labels = [d.strftime('%d.%m') for d in dates]
            ax2.set_xticks(range(len(dates)))
            ax2.set_xticklabels(date_labels, rotation=45, ha='right')

        fig.suptitle('Анализ сна: Длительность и качество', color='white', y=0.98)
        fig.tight_layout(rect=[0, 0, 1, 0.96])

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def clear_graph_frame(self):
        """Очистка фрейма с графиками"""
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

    def export_data(self):
        """Экспорт данных в файл"""
        if not self.sleep_data:
            messagebox.showwarning("Внимание", "Нет данных для экспорта")
            return

        try:
            # Создаем текстовый отчет
            report = "=" * 50 + "\n"
            report += "ОТЧЕТ ПО СНУ\n"
            report += f"Сгенерирован: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
            report += "=" * 50 + "\n\n"

            # Общая статистика
            total_records = len(self.sleep_data)
            total_duration_hours = sum(r['duration_hours'] for r in self.sleep_data)
            avg_duration_hours = total_duration_hours / total_records
            avg_quality = sum(r['quality'] for r in self.sleep_data) / total_records

            report += "ОБЩАЯ СТАТИСТИКА:\n"
            report += f"- Всего записей: {total_records}\n"
            report += f"- Средняя длительность: {avg_duration_hours:.1f} часов\n"
            report += f"- Среднее качество: {avg_quality:.1f}/10\n\n"

            # Подробные записи
            report += "ПОДРОБНЫЕ ЗАПИСИ:\n"
            report += "Дата       | Время сна  | Длит. | Кач. | Комментарии\n"
            report += "-" * 60 + "\n"

            for record in sorted(self.sleep_data, key=lambda x: x['date'], reverse=True):
                date_str = record['date'].strftime('%d.%m.%Y')
                sleep_time = f"{record['bedtime']}-{record['wakeup']}"
                quality_str = f"{record['quality']}/10"
                comment = record['comments'][:30] + "..." if len(record['comments']) > 30 else record['comments']

                report += f"{date_str} | {sleep_time:11} | {record['duration']:5} | {quality_str:5} | {comment}\n"

            # Сохранение в файл
            filename = f"sleep_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report)

            messagebox.showinfo("Успех", f"Данные экспортированы в файл:\n{filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные:\n{str(e)}")


def main():
    # Проверка наличия необходимых библиотек
    try:
        import matplotlib
        import numpy as np
    except ImportError as e:
        print(f"Ошибка: Не установлена необходимая библиотека: {e}")
        print("Установите библиотеки командой:")
        print("pip install matplotlib numpy")
        return

    root = tk.Tk()
    app = SleepTrackerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()