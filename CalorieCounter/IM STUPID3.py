import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np


class CalorieCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍎 Calorie Counter - Счетчик калорий и диета")
        self.root.geometry("1300x800")
        self.root.configure(bg="#f0f8ff")

        # Инициализация данных
        self.user_data = {}
        self.food_database = []
        self.daily_logs = {}
        self.current_date = datetime.now().date()

        # Загрузка данных
        self.load_data()

        # Настройка стилей
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
            'bg_main': '#f0f8ff',
            'bg_card': '#ffffff',
            'bg_dark': '#2c3e50',
            'accent_green': '#27ae60',
            'accent_red': '#e74c3c',
            'accent_blue': '#3498db',
            'accent_orange': '#f39c12',
            'text_dark': '#2c3e50',
            'text_light': '#ffffff',
            'success': '#2ecc71',
            'warning': '#f1c40f',
            'danger': '#e74c3c'
        }

        # Настройка стилей фреймов
        self.style.configure('Main.TFrame', background=self.colors['bg_main'])
        self.style.configure('Card.TFrame',
                             background=self.colors['bg_card'],
                             relief='solid',
                             borderwidth=1)
        self.style.configure('Dark.TFrame', background=self.colors['bg_dark'])

        # Стили для меток
        self.style.configure('Title.TLabel',
                             font=('Arial', 20, 'bold'),
                             background=self.colors['bg_main'],
                             foreground=self.colors['text_dark'])

        self.style.configure('Subtitle.TLabel',
                             font=('Arial', 12, 'bold'),
                             background=self.colors['bg_card'],
                             foreground=self.colors['text_dark'])

        self.style.configure('Stats.TLabel',
                             font=('Arial', 10),
                             background=self.colors['bg_card'],
                             foreground=self.colors['text_dark'])

        # Стили для кнопок
        self.style.configure('Success.TButton',
                             font=('Arial', 10, 'bold'),
                             background=self.colors['success'],
                             foreground=self.colors['text_light'])

        self.style.configure('Primary.TButton',
                             font=('Arial', 10, 'bold'),
                             background=self.colors['accent_blue'],
                             foreground=self.colors['text_light'])

        self.style.configure('Warning.TButton',
                             font=('Arial', 10, 'bold'),
                             background=self.colors['warning'],
                             foreground=self.colors['text_dark'])

        # Стили для прогресс-баров
        self.style.configure('Green.Horizontal.TProgressbar',
                             background=self.colors['success'])
        self.style.configure('Yellow.Horizontal.TProgressbar',
                             background=self.colors['warning'])
        self.style.configure('Red.Horizontal.TProgressbar',
                             background=self.colors['danger'])
        self.style.configure('Blue.Horizontal.TProgressbar',
                             background=self.colors['accent_blue'])

        # Конфигурация hover эффектов
        self.style.map('Success.TButton',
                       background=[('active', '#25a25a')])
        self.style.map('Primary.TButton',
                       background=[('active', '#2980b9')])
        self.style.map('Warning.TButton',
                       background=[('active', '#e67e22')])

    def load_data(self):
        """Загрузка данных из файлов"""
        # Загрузка данных пользователя
        if os.path.exists("user_data.json"):
            try:
                with open("user_data.json", "r", encoding="utf-8") as f:
                    self.user_data = json.load(f)
            except:
                self.user_data = {}
        else:
            self.user_data = {}

        # Загрузка базы данных продуктов
        if os.path.exists("food_database.json"):
            try:
                with open("food_database.json", "r", encoding="utf-8") as f:
                    self.food_database = json.load(f)
            except:
                self.food_database = self.create_default_food_database()
        else:
            self.food_database = self.create_default_food_database()

        # Загрузка дневных логов
        if os.path.exists("daily_logs.json"):
            try:
                with open("daily_logs.json", "r", encoding="utf-8") as f:
                    self.daily_logs = json.load(f)
            except:
                self.daily_logs = {}

        # Конвертация дат в объекты datetime.date
        for date_str in list(self.daily_logs.keys()):
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                # Создаем новый ключ с объектом даты
                self.daily_logs[date_obj] = self.daily_logs.pop(date_str)
            except:
                continue

    def create_default_food_database(self):
        """Создание стандартной базы данных продуктов"""
        return [
            {
                "name": "Куриная грудка",
                "category": "Мясо и птица",
                "calories": 165,
                "protein": 31,
                "carbs": 0,
                "fat": 3.6,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Говядина",
                "category": "Мясо и птица",
                "calories": 250,
                "protein": 26,
                "carbs": 0,
                "fat": 17,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Яйцо куриное",
                "category": "Яйца и молочные",
                "calories": 155,
                "protein": 13,
                "carbs": 1.1,
                "fat": 11,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Творог 5%",
                "category": "Яйца и молочные",
                "calories": 121,
                "protein": 17,
                "carbs": 1.8,
                "fat": 5,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Рис отварной",
                "category": "Крупы и злаки",
                "calories": 130,
                "protein": 2.7,
                "carbs": 28,
                "fat": 0.3,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Гречка отварная",
                "category": "Крупы и злаки",
                "calories": 110,
                "protein": 4.5,
                "carbs": 21,
                "fat": 1.3,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Картофель отварной",
                "category": "Овощи",
                "calories": 86,
                "protein": 1.7,
                "carbs": 18,
                "fat": 0.1,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Брокколи",
                "category": "Овощи",
                "calories": 34,
                "protein": 2.8,
                "carbs": 6.6,
                "fat": 0.4,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Яблоко",
                "category": "Фрукты",
                "calories": 52,
                "protein": 0.3,
                "carbs": 14,
                "fat": 0.2,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Банан",
                "category": "Фрукты",
                "calories": 89,
                "protein": 1.1,
                "carbs": 23,
                "fat": 0.3,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Хлеб пшеничный",
                "category": "Хлеб и выпечка",
                "calories": 265,
                "protein": 7.7,
                "carbs": 53,
                "fat": 1.3,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Оливковое масло",
                "category": "Жиры и масла",
                "calories": 884,
                "protein": 0,
                "carbs": 0,
                "fat": 100,
                "portion_size": 100,
                "unit": "мл"
            },
            {
                "name": "Молоко 2.5%",
                "category": "Напитки",
                "calories": 52,
                "protein": 2.9,
                "carbs": 4.7,
                "fat": 2.5,
                "portion_size": 100,
                "unit": "мл"
            },
            {
                "name": "Вода",
                "category": "Напитки",
                "calories": 0,
                "protein": 0,
                "carbs": 0,
                "fat": 0,
                "portion_size": 100,
                "unit": "мл"
            },
            {
                "name": "Шоколад молочный",
                "category": "Сладости",
                "calories": 535,
                "protein": 7.7,
                "carbs": 59,
                "fat": 30,
                "portion_size": 100,
                "unit": "г"
            },
            {
                "name": "Печенье овсяное",
                "category": "Сладости",
                "calories": 450,
                "protein": 6.5,
                "carbs": 74,
                "fat": 16,
                "portion_size": 100,
                "unit": "г"
            }
        ]

    def save_data(self):
        """Сохранение данных в файлы"""
        # Сохранение данных пользователя
        with open("user_data.json", "w", encoding="utf-8") as f:
            json.dump(self.user_data, f, ensure_ascii=False, indent=2)

        # Сохранение базы данных продуктов
        with open("food_database.json", "w", encoding="utf-8") as f:
            json.dump(self.food_database, f, ensure_ascii=False, indent=2)

        # Конвертация дат обратно в строки для сохранения
        save_logs = {}
        for date_obj, log_data in self.daily_logs.items():
            if isinstance(date_obj, datetime):
                date_str = date_obj.strftime('%Y-%m-%d')
            elif hasattr(date_obj, 'strftime'):
                date_str = date_obj.strftime('%Y-%m-%d')
            else:
                date_str = str(date_obj)
            save_logs[date_str] = log_data

        with open("daily_logs.json", "w", encoding="utf-8") as f:
            json.dump(save_logs, f, ensure_ascii=False, indent=2)

    def create_widgets(self):
        """Создание интерфейса приложения"""
        # Основной контейнер
        main_container = ttk.Frame(self.root, style='Main.TFrame', padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        header_frame = ttk.Frame(main_container, style='Card.TFrame')
        header_frame.grid(row=0, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 15))

        title_label = ttk.Label(header_frame,
                                text="🍎 Счетчик калорий и диета",
                                style='Title.TLabel')
        title_label.pack(pady=10)

        # Основное содержимое
        content_frame = ttk.Frame(main_container, style='Main.TFrame')
        content_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Левая панель - профиль и добавление еды
        left_panel = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        left_panel.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Средняя панель - статистика и графики
        middle_panel = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        middle_panel.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Правая панель - дневник и история
        right_panel = ttk.Frame(content_frame, style='Card.TFrame', padding="15")
        right_panel.grid(row=0, column=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Настройка весов для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        content_frame.columnconfigure(2, weight=1)
        content_frame.rowconfigure(0, weight=1)

        # === ЛЕВАЯ ПАНЕЛЬ: Профиль и добавление еды ===
        left_title = ttk.Label(left_panel, text="👤 Профиль и добавление еды",
                               style='Subtitle.TLabel')
        left_title.grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))

        # Информация о пользователе
        user_info_frame = ttk.Frame(left_panel, style='Card.TFrame', padding="10")
        user_info_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Label(user_info_frame, text="Данные пользователя:",
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Поля для ввода данных пользователя
        ttk.Label(user_info_frame, text="Цель (ккал/день):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.calorie_goal_var = tk.StringVar(value="2000")
        ttk.Entry(user_info_frame, textvariable=self.calorie_goal_var, width=15).grid(row=1, column=1, sticky=tk.W,
                                                                                      pady=5, padx=(10, 0))

        ttk.Label(user_info_frame, text="Белки (г/день):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.protein_goal_var = tk.StringVar(value="120")
        ttk.Entry(user_info_frame, textvariable=self.protein_goal_var, width=15).grid(row=2, column=1, sticky=tk.W,
                                                                                      pady=5, padx=(10, 0))

        ttk.Label(user_info_frame, text="Жиры (г/день):").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.fat_goal_var = tk.StringVar(value="70")
        ttk.Entry(user_info_frame, textvariable=self.fat_goal_var, width=15).grid(row=3, column=1, sticky=tk.W, pady=5,
                                                                                  padx=(10, 0))

        ttk.Label(user_info_frame, text="Углеводы (г/день):").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.carbs_goal_var = tk.StringVar(value="250")
        ttk.Entry(user_info_frame, textvariable=self.carbs_goal_var, width=15).grid(row=4, column=1, sticky=tk.W,
                                                                                    pady=5, padx=(10, 0))

        # Кнопка сохранения настроек
        save_profile_btn = ttk.Button(user_info_frame, text="💾 Сохранить настройки",
                                      style='Primary.TButton',
                                      command=self.save_user_profile)
        save_profile_btn.grid(row=5, column=0, columnspan=2, pady=(10, 0))

        # Добавление еды
        add_food_frame = ttk.Frame(left_panel, style='Card.TFrame', padding="10")
        add_food_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Label(add_food_frame, text="Добавить прием пищи:",
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # Выбор продукта
        ttk.Label(add_food_frame, text="Продукт:").grid(row=1, column=0, sticky=tk.W, pady=5)

        # Создаем список продуктов для Combobox
        food_names = [f"{food['name']} ({food['calories']} ккал/100г)" for food in self.food_database]
        self.food_combo_var = tk.StringVar()
        self.food_combo = ttk.Combobox(add_food_frame, textvariable=self.food_combo_var,
                                       values=food_names, width=25, state="readonly")
        self.food_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Количество
        ttk.Label(add_food_frame, text="Количество (г/мл):").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.quantity_var = tk.StringVar(value="100")
        ttk.Entry(add_food_frame, textvariable=self.quantity_var, width=15).grid(row=2, column=1, sticky=tk.W, pady=5,
                                                                                 padx=(10, 0))

        # Прием пищи
        ttk.Label(add_food_frame, text="Прием пищи:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.meal_type_var = tk.StringVar(value="Завтрак")
        meal_combo = ttk.Combobox(add_food_frame, textvariable=self.meal_type_var,
                                  values=["Завтрак", "Обед", "Ужин", "Перекус"], width=15, state="readonly")
        meal_combo.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Кнопка добавления
        add_food_btn = ttk.Button(add_food_frame, text="➕ Добавить продукт",
                                  style='Success.TButton',
                                  command=self.add_food_to_log)
        add_food_btn.grid(row=4, column=0, columnspan=2, pady=(10, 0))

        # Быстрое добавление воды
        water_frame = ttk.Frame(left_panel, style='Card.TFrame', padding="10")
        water_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        ttk.Label(water_frame, text="💧 Вода:",
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 10))

        ttk.Label(water_frame, text="Количество (мл):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.water_var = tk.StringVar(value="250")
        ttk.Entry(water_frame, textvariable=self.water_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5,
                                                                           padx=(10, 0))

        add_water_btn = ttk.Button(water_frame, text="➕ Добавить воду",
                                   style='Primary.TButton',
                                   command=self.add_water)
        add_water_btn.grid(row=2, column=0, columnspan=2, pady=(10, 0))

        # Добавление нового продукта
        new_food_frame = ttk.Frame(left_panel, style='Card.TFrame', padding="10")
        new_food_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Label(new_food_frame, text="➕ Добавить новый продукт:",
                  font=('Arial', 10, 'bold')).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        add_new_food_btn = ttk.Button(new_food_frame, text="Создать новый продукт",
                                      style='Warning.TButton',
                                      command=self.show_add_food_dialog)
        add_new_food_btn.grid(row=1, column=0, columnspan=2, pady=(5, 0))

        # === СРЕДНЯЯ ПАНЕЛЬ: Статистика и графики ===
        middle_title = ttk.Label(middle_panel, text="📊 Статистика и прогресс",
                                 style='Subtitle.TLabel')
        middle_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))

        # Статистика за сегодня
        stats_frame = ttk.Frame(middle_panel, style='Card.TFrame', padding="15")
        stats_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))

        # Заголовок с датой
        date_str = self.current_date.strftime('%d.%m.%Y')
        self.date_label = ttk.Label(stats_frame, text=f"📅 {date_str}",
                                    font=('Arial', 11, 'bold'))
        self.date_label.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 15))

        # Кнопки навигации по датам
        nav_frame = ttk.Frame(stats_frame)
        nav_frame.grid(row=0, column=3, columnspan=2, sticky=tk.E)

        ttk.Button(nav_frame, text="◀", width=3,
                   command=lambda: self.change_date(-1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="▶", width=3,
                   command=lambda: self.change_date(1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(nav_frame, text="Сегодня", width=8,
                   command=lambda: self.change_date(0)).pack(side=tk.LEFT, padx=2)

        # Статистические метки
        self.stats_labels = {}
        self.progress_bars = {}  # Новый словарь для прогресс-баров

        stats_items = [
            ("Калории:", "calories", "ккал"),
            ("Белки:", "protein", "г"),
            ("Жиры:", "fat", "г"),
            ("Углеводы:", "carbs", "г")
        ]

        for i, (label_text, key, unit) in enumerate(stats_items):
            # Название
            ttk.Label(stats_frame, text=label_text,
                      font=('Arial', 10)).grid(row=i + 1, column=0, sticky=tk.W, pady=5)

            # Прогресс бар
            progress_var = tk.DoubleVar(value=0)
            progress_bar = ttk.Progressbar(stats_frame, variable=progress_var,
                                           maximum=100, length=150,
                                           style='Blue.Horizontal.TProgressbar')
            progress_bar.grid(row=i + 1, column=1, sticky=tk.W, pady=5, padx=(10, 10))

            # Сохранение ссылки на прогресс-бар
            self.progress_bars[key] = progress_bar

            # Текущее значение
            value_label = ttk.Label(stats_frame, text="0/0",
                                    font=('Arial', 10, 'bold'))
            value_label.grid(row=i + 1, column=2, sticky=tk.W, pady=5)

            # Единицы измерения
            ttk.Label(stats_frame, text=unit).grid(row=i + 1, column=3, sticky=tk.W, pady=5)

            # Сохранение ссылок
            self.stats_labels[f"{key}_progress"] = progress_var
            self.stats_labels[f"{key}_value"] = value_label

        # Вода
        ttk.Label(stats_frame, text="Вода:",
                  font=('Arial', 10)).grid(row=5, column=0, sticky=tk.W, pady=5)

        water_progress_var = tk.DoubleVar(value=0)
        water_progress = ttk.Progressbar(stats_frame, variable=water_progress_var,
                                         maximum=100, length=150,
                                         style='Blue.Horizontal.TProgressbar')
        water_progress.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 10))

        self.progress_bars["water"] = water_progress

        water_value_label = ttk.Label(stats_frame, text="0/2000 мл",
                                      font=('Arial', 10, 'bold'))
        water_value_label.grid(row=5, column=2, sticky=tk.W, pady=5)

        self.stats_labels["water_progress"] = water_progress_var
        self.stats_labels["water_value"] = water_value_label

        # Круговая диаграмма БЖУ
        self.nutrition_chart_frame = ttk.Frame(middle_panel, style='Card.TFrame', padding="10")
        self.nutrition_chart_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 15))

        # График калорий за неделю
        self.calories_chart_frame = ttk.Frame(middle_panel, style='Card.TFrame', padding="10")
        self.calories_chart_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Инициализация графиков
        self.update_charts()

        # === ПРАВАЯ ПАНЕЛЬ: Дневник и история ===
        right_title = ttk.Label(right_panel, text="📝 Дневник питания",
                                style='Subtitle.TLabel')
        right_title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))

        # Таблица приемов пищи
        columns = ("meal", "food", "quantity", "calories")
        self.food_log_tree = ttk.Treeview(right_panel, columns=columns,
                                          show="headings", height=15)

        self.food_log_tree.heading("meal", text="Прием пищи")
        self.food_log_tree.heading("food", text="Продукт")
        self.food_log_tree.heading("quantity", text="Количество")
        self.food_log_tree.heading("calories", text="Калории")

        self.food_log_tree.column("meal", width=80)
        self.food_log_tree.column("food", width=150)
        self.food_log_tree.column("quantity", width=80)
        self.food_log_tree.column("calories", width=70)

        # Стилизация таблицы
        self.style.configure("Treeview",
                             background=self.colors['bg_card'],
                             foreground=self.colors['text_dark'],
                             fieldbackground=self.colors['bg_card'],
                             rowheight=25)

        self.style.configure("Treeview.Heading",
                             background=self.colors['accent_blue'],
                             foreground=self.colors['text_light'],
                             font=('Arial', 9, 'bold'))

        # Скроллбар для таблицы
        tree_scrollbar = ttk.Scrollbar(right_panel, orient="vertical",
                                       command=self.food_log_tree.yview)
        self.food_log_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.food_log_tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        tree_scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S), pady=(0, 10))

        # Кнопки управления дневником
        diary_buttons_frame = ttk.Frame(right_panel)
        diary_buttons_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E))

        ttk.Button(diary_buttons_frame, text="🗑️ Удалить запись",
                   command=self.delete_food_entry).pack(side=tk.LEFT, padx=2)
        ttk.Button(diary_buttons_frame, text="📤 Экспорт дня",
                   command=self.export_daily_log).pack(side=tk.LEFT, padx=2)

        # Общие рекомендации
        recommendations_frame = ttk.Frame(right_panel, style='Card.TFrame', padding="10")
        recommendations_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

        ttk.Label(recommendations_frame, text="💡 Рекомендации:",
                  font=('Arial', 11, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        self.recommendations_text = tk.Text(recommendations_frame, height=6, width=40,
                                            wrap=tk.WORD, font=('Arial', 9),
                                            bg=self.colors['bg_card'],
                                            fg=self.colors['text_dark'],
                                            relief='flat')
        self.recommendations_text.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Загрузка данных текущего дня
        self.load_current_day_data()

    def save_user_profile(self):
        """Сохранение данных пользователя"""
        try:
            # Получение значений целей
            calorie_goal = int(self.calorie_goal_var.get())
            protein_goal = int(self.protein_goal_var.get())
            fat_goal = int(self.fat_goal_var.get())
            carbs_goal = int(self.carbs_goal_var.get())

            # Проверка валидности
            if calorie_goal <= 0 or protein_goal < 0 or fat_goal < 0 or carbs_goal < 0:
                messagebox.showerror("Ошибка", "Значения должны быть положительными числами")
                return

            # Сохранение в объект пользователя
            self.user_data['calorie_goal'] = calorie_goal
            self.user_data['protein_goal'] = protein_goal
            self.user_data['fat_goal'] = fat_goal
            self.user_data['carbs_goal'] = carbs_goal

            # Сохранение в файл
            self.save_data()

            # Обновление статистики
            self.update_statistics()

            messagebox.showinfo("Успех", "Настройки профиля сохранены!")

        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректные числовые значения")

    def add_food_to_log(self):
        """Добавление продукта в дневник"""
        # Получение выбранного продукта
        selected_food_str = self.food_combo_var.get()
        if not selected_food_str:
            messagebox.showwarning("Внимание", "Выберите продукт")
            return

        # Извлечение названия продукта
        food_name = selected_food_str.split(" (")[0]

        # Поиск продукта в базе данных
        food_item = None
        for food in self.food_database:
            if food['name'] == food_name:
                food_item = food
                break

        if not food_item:
            messagebox.showerror("Ошибка", "Продукт не найден в базе данных")
            return

        # Получение количества
        try:
            quantity = float(self.quantity_var.get())
            if quantity <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество")
            return

        # Получение типа приема пищи
        meal_type = self.meal_type_var.get()

        # Расчет питательных веществ
        multiplier = quantity / 100  # Так как данные на 100г

        calories = food_item['calories'] * multiplier
        protein = food_item['protein'] * multiplier
        fat = food_item['fat'] * multiplier
        carbs = food_item['carbs'] * multiplier

        # Создание записи
        food_entry = {
            'name': food_item['name'],
            'meal_type': meal_type,
            'quantity': quantity,
            'unit': food_item['unit'],
            'calories': round(calories, 1),
            'protein': round(protein, 1),
            'fat': round(fat, 1),
            'carbs': round(carbs, 1),
            'timestamp': datetime.now().strftime('%H:%M')
        }

        # Добавление в дневник текущего дня
        date_key = self.current_date

        if date_key not in self.daily_logs:
            self.daily_logs[date_key] = {
                'foods': [],
                'water': 0,
                'total_calories': 0,
                'total_protein': 0,
                'total_fat': 0,
                'total_carbs': 0
            }

        # Добавление записи
        self.daily_logs[date_key]['foods'].append(food_entry)

        # Обновление общих значений
        self.daily_logs[date_key]['total_calories'] += food_entry['calories']
        self.daily_logs[date_key]['total_protein'] += food_entry['protein']
        self.daily_logs[date_key]['total_fat'] += food_entry['fat']
        self.daily_logs[date_key]['total_carbs'] += food_entry['carbs']

        # Сохранение данных
        self.save_data()

        # Обновление интерфейса
        self.load_current_day_data()
        self.update_statistics()
        self.update_charts()

        # Очистка полей
        self.quantity_var.set("100")
        messagebox.showinfo("Успех", f"Продукт '{food_name}' добавлен в {meal_type.lower()}")

    def add_water(self):
        """Добавление воды в дневник"""
        try:
            water_amount = int(self.water_var.get())
            if water_amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректное количество воды")
            return

        # Добавление в дневник текущего дня
        date_key = self.current_date

        if date_key not in self.daily_logs:
            self.daily_logs[date_key] = {
                'foods': [],
                'water': 0,
                'total_calories': 0,
                'total_protein': 0,
                'total_fat': 0,
                'total_carbs': 0
            }

        # Добавление воды
        self.daily_logs[date_key]['water'] += water_amount

        # Сохранение данных
        self.save_data()

        # Обновление интерфейса
        self.update_statistics()

        messagebox.showinfo("Успех", f"Добавлено {water_amount} мл воды")

    def show_add_food_dialog(self):
        """Отображение диалога добавления нового продукта"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить новый продукт")
        dialog.geometry("400x500")
        dialog.configure(bg=self.colors['bg_main'])
        dialog.transient(self.root)
        dialog.grab_set()

        # Фрейм для формы
        form_frame = ttk.Frame(dialog, style='Card.TFrame', padding="20")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="Добавить новый продукт",
                  font=('Arial', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Поля формы
        fields = [
            ("Название продукта:", "name", tk.StringVar()),
            ("Категория:", "category", tk.StringVar(value="Другое")),
            ("Калории (на 100г):", "calories", tk.StringVar()),
            ("Белки (г на 100г):", "protein", tk.StringVar()),
            ("Жиры (г на 100г):", "fat", tk.StringVar()),
            ("Углеводы (г на 100г):", "carbs", tk.StringVar()),
            ("Размер порции:", "portion_size", tk.StringVar(value="100")),
            ("Единица измерения:", "unit", tk.StringVar(value="г"))
        ]

        self.dialog_vars = {}

        for i, (label_text, key, var) in enumerate(fields):
            ttk.Label(form_frame, text=label_text).grid(row=i + 1, column=0, sticky=tk.W, pady=5)

            if key == "category":
                # Combobox для категории
                categories = ["Мясо и птица", "Рыба и морепродукты", "Яйца и молочные",
                              "Овощи", "Фрукты", "Крупы и злаки", "Хлеб и выпечка",
                              "Жиры и масла", "Напитки", "Сладости", "Другое"]
                combo = ttk.Combobox(form_frame, textvariable=var, values=categories, state="readonly")
                combo.grid(row=i + 1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
            else:
                entry = ttk.Entry(form_frame, textvariable=var, width=20)
                entry.grid(row=i + 1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

            self.dialog_vars[key] = var

        # Кнопки
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields) + 2, column=0, columnspan=2, pady=(20, 0))

        def save_new_food():
            """Сохранение нового продукта"""
            try:
                # Валидация данных
                if not self.dialog_vars['name'].get().strip():
                    messagebox.showerror("Ошибка", "Введите название продукта")
                    return

                # Проверка числовых значений
                numeric_fields = ['calories', 'protein', 'fat', 'carbs', 'portion_size']
                for field in numeric_fields:
                    try:
                        value = float(self.dialog_vars[field].get())
                        if value < 0:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Ошибка", f"Введите корректное значение для {field}")
                        return

                # Создание нового продукта
                new_food = {
                    'name': self.dialog_vars['name'].get().strip(),
                    'category': self.dialog_vars['category'].get(),
                    'calories': float(self.dialog_vars['calories'].get()),
                    'protein': float(self.dialog_vars['protein'].get()),
                    'fat': float(self.dialog_vars['fat'].get()),
                    'carbs': float(self.dialog_vars['carbs'].get()),
                    'portion_size': float(self.dialog_vars['portion_size'].get()),
                    'unit': self.dialog_vars['unit'].get()
                }

                # Добавление в базу данных
                self.food_database.append(new_food)

                # Сохранение данных
                self.save_data()

                # Обновление списка продуктов
                food_names = [f"{food['name']} ({food['calories']} ккал/100г)" for food in self.food_database]
                self.food_combo['values'] = food_names

                dialog.destroy()
                messagebox.showinfo("Успех", f"Продукт '{new_food['name']}' добавлен в базу данных!")

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")

        ttk.Button(button_frame, text="Сохранить", style='Success.TButton',
                   command=save_new_food).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена",
                   command=dialog.destroy).pack(side=tk.LEFT, padx=5)

    def change_date(self, days_delta):
        """Изменение текущей даты"""
        if days_delta == 0:
            # Установка сегодняшней даты
            self.current_date = datetime.now().date()
        else:
            # Изменение даты на указанное количество дней
            self.current_date += timedelta(days=days_delta)

        # Обновление интерфейса
        self.load_current_day_data()
        self.update_statistics()
        self.update_charts()

    def load_current_day_data(self):
        """Загрузка данных текущего дня"""
        # Обновление метки даты
        date_str = self.current_date.strftime('%d.%m.%Y')
        self.date_label.config(text=f"📅 {date_str}")

        # Очистка таблицы
        for item in self.food_log_tree.get_children():
            self.food_log_tree.delete(item)

        # Загрузка данных дня
        date_key = self.current_date
        if date_key in self.daily_logs:
            day_data = self.daily_logs[date_key]

            # Добавление записей в таблицу
            for food_entry in day_data['foods']:
                values = (
                    food_entry['meal_type'],
                    food_entry['name'],
                    f"{food_entry['quantity']} {food_entry['unit']}",
                    f"{food_entry['calories']} ккал"
                )
                self.food_log_tree.insert("", tk.END, values=values)
        else:
            # Создание пустого дня
            self.daily_logs[date_key] = {
                'foods': [],
                'water': 0,
                'total_calories': 0,
                'total_protein': 0,
                'total_fat': 0,
                'total_carbs': 0
            }

    def update_statistics(self):
        """Обновление статистики и прогресс-баров"""
        # Получение целей из пользовательских данных
        calorie_goal = self.user_data.get('calorie_goal', 2000)
        protein_goal = self.user_data.get('protein_goal', 120)
        fat_goal = self.user_data.get('fat_goal', 70)
        carbs_goal = self.user_data.get('carbs_goal', 250)
        water_goal = 2000  # Стандартная норма воды

        # Получение текущих значений
        date_key = self.current_date
        if date_key in self.daily_logs:
            day_data = self.daily_logs[date_key]
            current_calories = day_data['total_calories']
            current_protein = day_data['total_protein']
            current_fat = day_data['total_fat']
            current_carbs = day_data['total_carbs']
            current_water = day_data['water']
        else:
            current_calories = current_protein = current_fat = current_carbs = current_water = 0

        # Обновление прогресс-баров и меток
        stats_data = [
            (current_calories, calorie_goal, "calories", "ккал"),
            (current_protein, protein_goal, "protein", "г"),
            (current_fat, fat_goal, "fat", "г"),
            (current_carbs, carbs_goal, "carbs", "г")
        ]

        for current, goal, key, unit in stats_data:
            progress = (current / goal * 100) if goal > 0 else 0

            # Ограничение прогресса 100%
            if progress > 100:
                progress = 100

            # Обновление прогресс-бара
            self.stats_labels[f"{key}_progress"].set(progress)

            # Обновление метки значения
            value_text = f"{current:.0f}/{goal} {unit}"
            self.stats_labels[f"{key}_value"].config(text=value_text)

            # Изменение цвета прогресс-бара в зависимости от заполнения
            if key in self.progress_bars:
                if progress > 100:
                    self.progress_bars[key].configure(style='Red.Horizontal.TProgressbar')
                elif progress > 90:
                    self.progress_bars[key].configure(style='Yellow.Horizontal.TProgressbar')
                else:
                    self.progress_bars[key].configure(style='Green.Horizontal.TProgressbar')

        # Обновление воды
        water_progress = (current_water / water_goal * 100) if water_goal > 0 else 0
        if water_progress > 100:
            water_progress = 100

        self.stats_labels["water_progress"].set(water_progress)
        self.stats_labels["water_value"].config(text=f"{current_water}/{water_goal} мл")

        # Изменение цвета прогресс-бара воды
        if "water" in self.progress_bars:
            if water_progress > 100:
                self.progress_bars["water"].configure(style='Red.Horizontal.TProgressbar')
            elif water_progress > 90:
                self.progress_bars["water"].configure(style='Yellow.Horizontal.TProgressbar')
            else:
                self.progress_bars["water"].configure(style='Green.Horizontal.TProgressbar')

        # Генерация рекомендаций
        recommendations = self.generate_recommendations(
            current_calories, calorie_goal,
            current_protein, protein_goal,
            current_fat, fat_goal,
            current_carbs, carbs_goal,
            current_water, water_goal
        )

        self.recommendations_text.delete("1.0", tk.END)
        self.recommendations_text.insert("1.0", recommendations)

    def generate_recommendations(self, cal, cal_goal, prot, prot_goal,
                                 fat, fat_goal, carbs, carbs_goal, water, water_goal):
        """Генерация рекомендаций на основе текущих данных"""
        recommendations = []

        # Рекомендации по калориям
        if cal == 0:
            recommendations.append("🍽️ Вы еще не добавили приемы пищи сегодня.")
            recommendations.append("Начните отслеживать свое питание!")
        elif cal < cal_goal * 0.7:
            recommendations.append(f"⚠️ Вы потребили только {cal:.0f} ккал из {cal_goal}.")
            recommendations.append("Рассмотрите возможность добавить полезный перекус.")
        elif cal > cal_goal * 1.1:
            recommendations.append(f"⚠️ Вы превысили дневную норму на {cal - cal_goal:.0f} ккал.")
            recommendations.append("Постарайтесь уменьшить порции на ужин.")
        else:
            recommendations.append("✅ Отличный баланс калорий!")

        # Рекомендации по БЖУ
        if prot < prot_goal * 0.8:
            recommendations.append(f"\n🥩 Не хватает белков: {prot:.0f}г из {prot_goal}г.")
            recommendations.append("Добавьте курицу, рыбу, творог или яйца.")

        if fat < fat_goal * 0.8:
            recommendations.append(f"\n🥑 Не хватает жиров: {fat:.0f}г из {fat_goal}г.")
            recommendations.append("Добавьте орехи, авокадо или оливковое масло.")
        elif fat > fat_goal * 1.2:
            recommendations.append(f"\n🥑 Много жиров: {fat:.0f}г из {fat_goal}г.")
            recommendations.append("Уменьшите потребление масла и жирных продуктов.")

        if carbs < carbs_goal * 0.8:
            recommendations.append(f"\n🍚 Не хватает углеводов: {carbs:.0f}г из {carbs_goal}г.")
            recommendations.append("Добавьте крупы, хлеб или фрукты.")

        # Рекомендации по воде
        if water < water_goal * 0.5:
            recommendations.append(f"\n💧 Выпито только {water} мл воды.")
            recommendations.append("Старайтесь выпивать 2 литра воды в день!")
        elif water < water_goal:
            recommendations.append(f"\n💧 Выпито {water} мл воды.")
            recommendations.append(f"Осталось {water_goal - water} мл до нормы.")
        else:
            recommendations.append("\n💧 Отличная гидратация!")

        # Общие рекомендации
        recommendations.append("\n💡 Общие советы:")
        recommendations.append("• Ешьте больше овощей и фруктов")
        recommendations.append("• Избегайте переработанных продуктов")
        recommendations.append("• Питайтесь регулярно 3-5 раз в день")
        recommendations.append("• Не забывайте про физическую активность")

        return "\n".join(recommendations)

    def update_charts(self):
        """Обновление графиков"""
        self.update_nutrition_chart()
        self.update_calories_chart()

    def update_nutrition_chart(self):
        """Обновление круговой диаграммы БЖУ"""
        # Очистка фрейма
        for widget in self.nutrition_chart_frame.winfo_children():
            widget.destroy()

        # Получение данных текущего дня
        date_key = self.current_date
        if date_key in self.daily_logs:
            day_data = self.daily_logs[date_key]
            protein = day_data['total_protein']
            fat = day_data['total_fat']
            carbs = day_data['total_carbs']
            total = protein + fat + carbs

            if total > 0:
                # Создание круговой диаграммы
                fig = Figure(figsize=(5, 4), facecolor=self.colors['bg_card'])
                ax = fig.add_subplot(111)

                # Данные для диаграммы
                sizes = [protein * 4, fat * 9, carbs * 4]  # Калории от каждого макронутриента
                labels = ['Белки', 'Жиры', 'Углеводы']
                colors = ['#4CAF50', '#FF9800', '#2196F3']

                # Построение диаграммы
                ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
                ax.set_title('Распределение калорий по БЖУ', fontsize=12, pad=20)

                # Вставка в Tkinter
                canvas = FigureCanvasTkAgg(fig, master=self.nutrition_chart_frame)
                canvas.draw()
                canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            else:
                # Нет данных
                ttk.Label(self.nutrition_chart_frame,
                          text="Нет данных для построения диаграммы",
                          font=('Arial', 10)).pack(expand=True)
        else:
            ttk.Label(self.nutrition_chart_frame,
                      text="Нет данных для построения диаграммы",
                      font=('Arial', 10)).pack(expand=True)

    def update_calories_chart(self):
        """Обновление графика калорий за неделю"""
        # Очистка фрейма
        for widget in self.calories_chart_frame.winfo_children():
            widget.destroy()

        # Получение данных за последние 7 дней
        dates = []
        calories = []
        goals = []

        for i in range(6, -1, -1):
            date = self.current_date - timedelta(days=i)
            dates.append(date.strftime('%d.%m'))

            if date in self.daily_logs:
                calories.append(self.daily_logs[date]['total_calories'])
            else:
                calories.append(0)

            goals.append(self.user_data.get('calorie_goal', 2000))

        # Создание графика
        fig = Figure(figsize=(8, 4), facecolor=self.colors['bg_card'])
        ax = fig.add_subplot(111)

        # Индексы для оси X
        x = range(len(dates))

        # График потребленных калорий
        bars = ax.bar(x, calories, color=self.colors['accent_blue'], alpha=0.7, label='Потреблено')

        # Линия цели
        ax.plot(x, goals, color=self.colors['accent_red'], linewidth=2, marker='o', label='Цель')

        # Настройки графика
        ax.set_xlabel('Дата', fontsize=10)
        ax.set_ylabel('Калории', fontsize=10)
        ax.set_title('Калории за последние 7 дней', fontsize=12, pad=20)
        ax.set_xticks(x)
        ax.set_xticklabels(dates, rotation=45)
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Цвет баров в зависимости от превышения цели
        for i, (bar, cal, goal) in enumerate(zip(bars, calories, goals)):
            if cal > goal * 1.1:
                bar.set_color(self.colors['accent_red'])
            elif cal < goal * 0.9:
                bar.set_color(self.colors['warning'])

        # Вставка в Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.calories_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def delete_food_entry(self):
        """Удаление выбранной записи о еде"""
        selection = self.food_log_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите запись для удаления")
            return

        if messagebox.askyesno("Подтверждение", "Удалить выбранную запись?"):
            item = self.food_log_tree.item(selection[0])
            values = item['values']

            # Получение данных записи
            meal_type = values[0]
            food_name = values[1]
            quantity_str = values[2]

            # Извлечение количества
            try:
                quantity = float(quantity_str.split()[0])
            except:
                quantity = 0

            # Удаление записи из данных
            date_key = self.current_date
            if date_key in self.daily_logs:
                day_data = self.daily_logs[date_key]

                # Поиск и удаление записи
                for i, food_entry in enumerate(day_data['foods']):
                    if (food_entry['name'] == food_name and
                            food_entry['meal_type'] == meal_type and
                            abs(food_entry['quantity'] - quantity) < 0.1):
                        # Вычитание из общих значений
                        day_data['total_calories'] -= food_entry['calories']
                        day_data['total_protein'] -= food_entry['protein']
                        day_data['total_fat'] -= food_entry['fat']
                        day_data['total_carbs'] -= food_entry['carbs']

                        # Удаление записи
                        del day_data['foods'][i]

                        # Сохранение данных
                        self.save_data()

                        # Обновление интерфейса
                        self.load_current_day_data()
                        self.update_statistics()
                        self.update_charts()

                        messagebox.showinfo("Успех", "Запись удалена")
                        return

            messagebox.showerror("Ошибка", "Не удалось найти запись для удаления")

    def export_daily_log(self):
        """Экспорт данных текущего дня в файл"""
        date_key = self.current_date
        if date_key not in self.daily_logs or not self.daily_logs[date_key]['foods']:
            messagebox.showwarning("Внимание", "Нет данных для экспорта")
            return

        try:
            day_data = self.daily_logs[date_key]
            date_str = date_key.strftime('%d.%m.%Y')

            # Создание отчета
            report = "=" * 60 + "\n"
            report += f"ОТЧЕТ О ПИТАНИИ - {date_str}\n"
            report += "=" * 60 + "\n\n"

            # Общая статистика
            report += "📊 ОБЩАЯ СТАТИСТИКА:\n"
            report += f"• Калории: {day_data['total_calories']:.0f} ккал\n"
            report += f"• Белки: {day_data['total_protein']:.1f} г\n"
            report += f"• Жиры: {day_data['total_fat']:.1f} г\n"
            report += f"• Углеводы: {day_data['total_carbs']:.1f} г\n"
            report += f"• Вода: {day_data['water']} мл\n\n"

            # Детали по приемам пищи
            report += "🍽️ ПРИЕМЫ ПИЩИ:\n"

            # Группировка по приемам пищи
            meals = {}
            for food_entry in day_data['foods']:
                meal_type = food_entry['meal_type']
                if meal_type not in meals:
                    meals[meal_type] = []
                meals[meal_type].append(food_entry)

            for meal_type in ["Завтрак", "Обед", "Ужин", "Перекус"]:
                if meal_type in meals:
                    report += f"\n{meal_type.upper()}:\n"
                    report += "-" * 40 + "\n"

                    total_meal_calories = 0
                    for food_entry in meals[meal_type]:
                        report += f"• {food_entry['name']}: {food_entry['quantity']} {food_entry['unit']} "
                        report += f"({food_entry['calories']} ккал)\n"
                        total_meal_calories += food_entry['calories']

                    report += f"\nВсего в {meal_type.lower()}: {total_meal_calories:.0f} ккал\n"

            # Сохранение в файл
            filename = f"food_log_{date_key.strftime('%Y%m%d')}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(report)

            messagebox.showinfo("Успех", f"Отчет сохранен в файл:\n{filename}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось экспортировать данные:\n{str(e)}")


def main():
    # Проверка наличия необходимых библиотек
    try:
        import matplotlib
    except ImportError:
        print("Ошибка: Не установлена библиотека matplotlib")
        print("Установите библиотеку командой:")
        print("pip install matplotlib")
        return

    root = tk.Tk()
    app = CalorieCounterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
