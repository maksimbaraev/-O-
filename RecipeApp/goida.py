import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from tkinter import scrolledtext


class RecipeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍳 Рецепты по ингредиентам")
        self.root.geometry("1000x750")
        self.root.configure(bg="#f5f5f5")

        # База данных рецептов с полными описаниями
        self.recipes = []
        self.available_ingredients = []

        # Загружаем данные
        self.load_recipes()
        self.extract_ingredients()

        # Переменные для интерфейса
        self.selected_ingredients = []

        # Настраиваем стили
        self.setup_styles()

        # Создаем интерфейс
        self.create_widgets()

    def setup_styles(self):
        """Настраиваем стили для приложения"""
        style = ttk.Style()
        style.theme_use('clam')

        # Стили для виджетов
        style.configure('Title.TLabel',
                        font=('Arial', 18, 'bold'),
                        background='#f5f5f5',
                        foreground='#2c3e50')

        style.configure('Card.TFrame',
                        background='white',
                        relief='solid',
                        borderwidth=1)

        style.configure('Header.TLabel',
                        font=('Arial', 12, 'bold'),
                        background='white',
                        foreground='#2c3e50')

        style.configure('Ingredient.TCheckbutton',
                        font=('Arial', 10),
                        background='white')

        style.configure('Recipe.Treeview',
                        font=('Arial', 10),
                        rowheight=25)

        style.configure('Recipe.Treeview.Heading',
                        font=('Arial', 11, 'bold'),
                        background='#3498db',
                        foreground='white')

        style.map('Recipe.Treeview.Heading',
                  background=[('active', '#2980b9')])

    def load_recipes(self):
        """Загружаем рецепты из файла или создаем демо-данные с полными описаниями"""
        if os.path.exists("recipes.json"):
            try:
                with open("recipes.json", "r", encoding="utf-8") as f:
                    self.recipes = json.load(f)
                return
            except:
                pass

        # Демо-рецепты с полными подробными инструкциями
        self.recipes = [
            {
                "name": "Омлет с сыром и помидорами",
                "ingredients": ["яйца", "сыр", "помидоры", "соль", "молоко", "масло растительное", "перец черный",
                                "зелень"],
                "instructions": """Полное описание приготовления:

1. Подготовка ингредиентов:
   - Возьмите 3 крупных яйца
   - 1 средний помидор нарежьте кубиками
   - 50 г твердого сыра натрите на средней терке
   - 2 столовые ложки молока
   - Соль и перец по вкусу
   - Небольшой пучок зелени (укроп, петрушка)

2. Приготовление:
   - В миске взбейте яйца с молоком до однородной массы
   - Добавьте соль и перец, перемешайте
   - Разогрейте сковороду с 1 столовой ложкой растительного масла
   - Вылейте яичную смесь на сковороду
   - Равномерно распределите нарезанные помидоры
   - Посыпьте тертым сыром
   - Накройте крышкой и готовьте на среднем огне 5-7 минут

3. Подача:
   - Готовый омлет посыпьте свежей зеленью
   - Подавайте горячим с тостами или свежими овощами

Совет: Для более пышного омлета добавьте щепотку соды в яичную смесь.""",
                "cooking_time": "15 минут",
                "difficulty": "легко",
                "category": "завтрак"
            },
            {
                "name": "Салат греческий",
                "ingredients": ["помидоры", "огурцы", "сыр фета", "оливковое масло", "оливки", "лук красный", "соль",
                                "орегано", "перец черный"],
                "instructions": """Полное описание приготовления:

1. Подготовка овощей:
   - 2 крупных помидора нарежьте крупными дольками
   - 1 длинный огурец нарежьте полукружками
   - 1 небольшую красную луковицу нарежьте тонкими полукольцами
   - 150 г сыра фета нарежьте кубиками
   - 100 г оливок без косточек

2. Сборка салата:
   - В большой салатник выложите нарезанные помидоры
   - Добавьте огурцы и красный лук
   - Разложите кубики сыра фета
   - Добавьте оливки

3. Заправка:
   - 3 столовые ложки оливкового масла
   - Сок половины лимона
   - 1 чайная ложка сушеного орегано
   - Соль и свежемолотый черный перец по вкусу
   - Все ингредиенты для заправки взбейте венчиком

4. Подача:
   - Полейте салат заправкой
   - Аккуратно перемешайте, стараясь не помять ингредиенты
   - Дайте настояться 5-10 минут перед подачей
   - Украсьте свежим орегано

Совет: Для аутентичного вкуса используйте греческие оливки и оливковое масло extra virgin.""",
                "cooking_time": "20 минут",
                "difficulty": "легко",
                "category": "салат"
            },
            {
                "name": "Паста с томатным соусом",
                "ingredients": ["паста спагетти", "помидоры", "лук", "чеснок", "оливковое масло", "соль", "базилик",
                                "томатная паста", "сахар", "пармезан"],
                "instructions": """Полное описание приготовления:

1. Приготовление соуса:
   - 3 крупных помидора надрежьте крест-накрест
   - Ошпарьте кипятком и снимите кожицу
   - Мякоть измельчите в блендере
   - 1 среднюю луковицу мелко нарежьте
   - 3 зубчика чеснока пропустите через пресс
   - В сковороде разогрейте 2 столовые ложки оливкового масла
   - Обжарьте лук до прозрачности
   - Добавьте чеснок, жарьте 1 минуту
   - Добавьте 1 столовую ложку томатной пасты, обжарьте 2 минуты
   - Вылейте измельченные помидоры
   - Добавьте щепотку сахара, соль и перец по вкусу
   - Тушите под крышкой 20 минут на медленном огне

2. Приготовление пасты:
   - В большой кастрюле вскипятите 3 литра воды
   - Добавьте 1 столовую ложку соли
   - Варите спагетти согласно инструкции на упаковке (обычно 8-10 минут)
   - Откиньте на дуршлаг, сохраните 1/2 стакана воды от варки

3. Соединение:
   - Добавьте отваренные спагетти в соус
   - Если соус слишком густой, добавьте немного воды от варки пасты
   - Прогрейте 2-3 минуты, постоянно помешивая
   - Добавьте свежий базилик

4. Подача:
   - Разложите пасту по тарелкам
   - Посыпьте тертым пармезаном
   - Украсьте листиками базилика
   - Сбрызните оливковым маслом

Совет: Для более насыщенного вкуса добавьте в соус анчоусы или каперсы.""",
                "cooking_time": "35 минут",
                "difficulty": "средне",
                "category": "основное блюдо"
            },
            {
                "name": "Блины классические",
                "ingredients": ["мука", "яйца", "молоко", "сахар", "соль", "масло растительное", "масло сливочное",
                                "разрыхлитель"],
                "instructions": """Полное описание приготовления:

1. Приготовление теста:
   - В глубокой миске взбейте 2 яйца с 2 столовыми ложками сахара
   - Добавьте щепотку соли
   - Постепенно влейте 500 мл молока комнатной температуры
   - Просейте 200 г муки с 1 чайной ложкой разрыхлителя
   - Постепенно добавляйте муку в жидкую смесь, постоянно помешивая
   - Добавьте 2 столовые ложки растительного масла
   - Тщательно перемешайте до исчезновения комочков
   - Дайте тесту постоять 15-20 минут

2. Выпекание блинов:
   - Разогрейте сковороду на среднем огне
   - Смажьте сковороду небольшим количеством масла (только для первого блина)
   - Налейте половник теста в центр сковороды
   - Быстро распределите тесто, вращая сковороду
   - Жарьте 1-2 минуты до золотистого цвета
   - Переверните лопаткой и жарьте еще 30-40 секунд

3. Особенности:
   - Первый блин может получиться неидеальным - это нормально
   - Для тонких блинов используйте меньше теста
   - Каждый готовый блин смазывайте сливочным маслом

4. Подача:
   - Подавайте блины стопкой
   - К блинам подайте:
     * Сметану
     * Сгущенное молоко
     * Мед
     * Варенье
     * Красную икру

Совет: Для воздушных блинов добавьте в тесто газированную воду вместо части молока.""",
                "cooking_time": "40 минут",
                "difficulty": "средне",
                "category": "завтрак/десерт"
            },
            {
                "name": "Куриный суп с лапшой",
                "ingredients": ["курица", "картофель", "морковь", "лук", "соль", "лавровый лист", "укроп", "петрушка",
                                "вермишель", "перец горошком"],
                "instructions": """Полное описание приготовления:

1. Приготовление бульона:
   - 500 г курицы (крылья, бедра или целая курица) промойте
   - Залейте 2,5 литрами холодной воды
   - Доведите до кипения на сильном огне
   - Снимите пену, убавьте огонь
   - Добавьте 1 очищенную луковицу целиком
   - Варите 40 минут на медленном огне
   - Добавьте 1 морковь, нарезанную кружочками
   - Варите еще 20 минут

2. Подготовка овощей:
   - 3 картофелины очистите и нарежьте кубиками
   - 1 морковь натрите на крупной терке
   - 1 луковицу мелко нарежьте
   - Пучок зелени (укроп, петрушка) мелко порубите

3. Приготовление супа:
   - Достаньте курицу из бульона, отделите мясо от костей
   - Бульон процедите
   - Верните мясо в бульон
   - Добавьте картофель, варите 10 минут
   - Добавьте морковь и лук, варите еще 5 минут
   - Добавьте 100 г вермишели
   - Добавьте соль, 3 горошины перца, 2 лавровых листа
   - Варите 5 минут до готовности вермишели

4. Подача:
   - Выключите огонь, добавьте зелень
   - Накройте крышкой, дайте настояться 10 минут
   - Разливайте по тарелкам
   - Подавайте со сметаной и черным хлебом

Совет: Для более наваристого бульона используйте курицу с костями и добавляйте корень петрушки.""",
                "cooking_time": "1 час 20 минут",
                "difficulty": "легко",
                "category": "суп"
            },
            {
                "name": "Жареная картошка с грибами",
                "ingredients": ["картофель", "лук", "грибы шампиньоны", "масло растительное", "соль", "укроп",
                                "перец черный", "чеснок", "сметана"],
                "instructions": """Полное описание приготовления:

1. Подготовка ингредиентов:
   - 800 г картофеля очистите и нарежьте соломкой или кубиками
   - 300 г шампиньонов нарежьте пластинками
   - 2 крупные луковицы нарежьте полукольцами
   - 3 зубчика чеснока измельчите
   - Пучок укропа мелко порубите

2. Обжарка грибов:
   - Разогрейте сковороду с 2 столовыми ложками масла
   - Обжарьте грибы до золотистого цвета
   - Добавьте соль и перец
   - Переложите грибы в отдельную миску

3. Приготовление картофеля:
   - В ту же сковороду добавьте еще масло
   - Обжарьте лук до прозрачности
   - Добавьте картофель, распределите ровным слоем
   - Жарьте на среднем огне 10 минут без перемешивания
   - Затем перемешайте и жарьте еще 10 минут
   - Добавьте соль, перец и чеснок
   - Верните грибы в сковороду
   - Жарьте все вместе 5 минут

4. Подача:
   - Посыпьте свежим укропом
   - Подавайте горячей со сметаной
   - Можно добавить маринованные огурцы или квашеную капусту

Совет: Для хрустящей корочки не накрывайте картофель крышкой во время жарки.""",
                "cooking_time": "30 минут",
                "difficulty": "легко",
                "category": "гарнир"
            },
            {
                "name": "Сэндвич с ветчиной и сыром в тостере",
                "ingredients": ["хлеб тостовый", "ветчина", "сыр", "помидоры", "майонез", "горчица", "масло сливочное",
                                "салат листовой"],
                "instructions": """Полное описание приготовления:

1. Подготовка ингредиентов:
   - 8 ломтиков тостового хлеба
   - 200 г ветчины нарежьте тонкими ломтиками
   - 150 г сыра (чеддер или гауда) нарежьте тонкими ломтиками
   - 1 помидор нарежьте тонкими кружками
   - Листья салата промойте и обсушите

2. Сборка сэндвичей:
   - На 4 ломтика хлеба намажьте майонез
   - На оставшиеся 4 ломтика намажьте горчицу
   - На хлеб с майонезом выложите:
     * Лист салата
     * 2-3 ломтика ветчины
     * Кружки помидора
   - На хлеб с горчицей выложите ломтики сыра
   - Соедините половинки сэндвичей

3. Обжарка:
   - Разогрейте тостер или сковороду
   - Снаружи сэндвичи смажьте размягченным сливочным маслом
   - Обжаривайте в тостере 3-4 минуты до золотистой корочки
   - Или на сковороде по 2-3 минуты с каждой стороны под прессом

4. Подача:
   - Разрежьте сэндвичи по диагонали
   - Подавайте горячими
   - Можно добавить соленые огурчики или оливки

Варианты:
- Добавьте авокадо для кремовой текстуры
- Используйте разные сорта сыра
- Добавьте яйцо-пашот для бенедикт-версии""",
                "cooking_time": "15 минут",
                "difficulty": "очень легко",
                "category": "закуска"
            }
        ]

        # Сохраняем демо-рецепты в файл
        self.save_recipes()

    def save_recipes(self):
        """Сохраняем рецепты в файл"""
        with open("recipes.json", "w", encoding="utf-8") as f:
            json.dump(self.recipes, f, ensure_ascii=False, indent=2)

    def extract_ingredients(self):
        """Извлекаем все уникальные ингредиенты из рецептов"""
        all_ingredients = set()
        for recipe in self.recipes:
            for ingredient in recipe["ingredients"]:
                all_ingredients.add(ingredient.lower())

        self.available_ingredients = sorted(list(all_ingredients))

    def create_widgets(self):
        """Создаем виджеты интерфейса"""
        # Основной контейнер
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Заголовок
        title_frame = ttk.Frame(main_container, style='Card.TFrame')
        title_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))

        title_label = ttk.Label(title_frame, text="🍳 Кулинарный помощник: Рецепты по ингредиентам",
                                style='Title.TLabel')
        title_label.pack(pady=10)

        subtitle_label = ttk.Label(title_frame,
                                   text="Выберите ингредиенты, которые у вас есть, и найдите подходящие рецепты",
                                   font=('Arial', 10), background='white')
        subtitle_label.pack(pady=(0, 10))

        # Основное содержимое - два столбца
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Левый столбец - выбор ингредиентов
        left_frame = ttk.Frame(content_frame, style='Card.TFrame')
        left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 10))

        # Заголовок для ингредиентов
        ingredients_header = ttk.Label(left_frame, text="📋 Выберите ингредиенты:", style='Header.TLabel')
        ingredients_header.grid(row=0, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(10, 5))

        # Поиск ингредиентов
        search_frame = ttk.Frame(left_frame, style='Card.TFrame')
        search_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))

        ttk.Label(search_frame, text="Поиск:", background='white').grid(row=0, column=0, padx=(5, 2), pady=5)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.grid(row=0, column=1, padx=2, pady=5, sticky=(tk.W, tk.E))
        search_entry.bind('<KeyRelease>', self.filter_ingredients)

        # Фрейм для чекбоксов ингредиентов с прокруткой
        ingredients_canvas_frame = ttk.Frame(left_frame)
        ingredients_canvas_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))

        # Canvas и Scrollbar для ингредиентов
        canvas = tk.Canvas(ingredients_canvas_frame, height=250, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(ingredients_canvas_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Изначальное заполнение чекбоксов
        self.ingredient_vars = {}
        self.ingredient_checkboxes = []
        self.filtered_ingredients = self.available_ingredients.copy()
        self.create_ingredient_checkboxes()

        canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Кнопки управления выбором
        buttons_frame = ttk.Frame(left_frame)
        buttons_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        select_all_btn = ttk.Button(buttons_frame, text="Выбрать все", command=self.select_all_ingredients)
        select_all_btn.grid(row=0, column=0, padx=5)

        clear_all_btn = ttk.Button(buttons_frame, text="Снять все", command=self.clear_all_ingredients)
        clear_all_btn.grid(row=0, column=1, padx=5)

        # Выбранные ингредиенты
        selected_header = ttk.Label(left_frame, text="✅ Выбранные ингредиенты:", style='Header.TLabel')
        selected_header.grid(row=4, column=0, columnspan=2, sticky=tk.W, padx=10, pady=(5, 5))

        self.selected_listbox = tk.Listbox(left_frame, height=6, font=('Arial', 10),
                                           selectmode=tk.SINGLE, bg='white')
        self.selected_listbox.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S),
                                   padx=10, pady=(0, 10))

        # Правый столбец - управление и результаты
        right_frame = ttk.Frame(content_frame, style='Card.TFrame')
        right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Кнопки действий
        action_buttons_frame = ttk.Frame(right_frame)
        action_buttons_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=10, pady=10)

        find_recipes_btn = ttk.Button(action_buttons_frame, text="🔍 Найти рецепты",
                                      command=self.find_recipes, width=20)
        find_recipes_btn.grid(row=0, column=0, padx=5)

        add_recipe_btn = ttk.Button(action_buttons_frame, text="➕ Добавить рецепт",
                                    command=self.add_recipe, width=20)
        add_recipe_btn.grid(row=0, column=1, padx=5)

        # Результаты поиска
        results_header = ttk.Label(right_frame, text="📋 Найденные рецепты:", style='Header.TLabel')
        results_header.grid(row=1, column=0, sticky=tk.W, padx=10, pady=(5, 5))

        # Treeview для результатов
        columns = ("name", "time", "difficulty", "category")
        self.results_tree = ttk.Treeview(right_frame, columns=columns, show="headings",
                                         height=12, style='Recipe.Treeview')

        # Настройка колонок
        self.results_tree.heading("name", text="Название рецепта")
        self.results_tree.heading("time", text="Время")
        self.results_tree.heading("difficulty", text="Сложность")
        self.results_tree.heading("category", text="Категория")

        self.results_tree.column("name", width=250)
        self.results_tree.column("time", width=80, anchor=tk.CENTER)
        self.results_tree.column("difficulty", width=100, anchor=tk.CENTER)
        self.results_tree.column("category", width=120, anchor=tk.CENTER)

        # Добавляем скроллбар
        tree_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=tree_scrollbar.set)

        self.results_tree.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=10, pady=(0, 10))
        tree_scrollbar.grid(row=2, column=1, sticky=(tk.N, tk.S), pady=(0, 10))

        # Привязываем двойной клик для просмотра рецепта
        self.results_tree.bind("<Double-1>", self.show_recipe_details)

        # Статистика
        stats_frame = ttk.Frame(right_frame, style='Card.TFrame')
        stats_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), padx=10, pady=(0, 10))

        self.stats_label = ttk.Label(stats_frame,
                                     text=f"Всего рецептов: {len(self.recipes)} | Ингредиентов: {len(self.available_ingredients)}",
                                     background='white', font=('Arial', 9))
        self.stats_label.pack(pady=5)

        # Настройка веса для растягивания
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.columnconfigure(1, weight=1)
        main_container.rowconfigure(1, weight=1)
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=1)
        content_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(2, weight=1)
        left_frame.rowconfigure(5, weight=1)
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(2, weight=1)
        ingredients_canvas_frame.columnconfigure(0, weight=1)
        ingredients_canvas_frame.rowconfigure(0, weight=1)

    def create_ingredient_checkboxes(self):
        """Создает чекбоксы для ингредиентов"""
        # Очищаем старые чекбоксы
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        self.ingredient_vars.clear()
        self.ingredient_checkboxes.clear()

        # Создаем новые чекбоксы для отфильтрованных ингредиентов
        for i, ingredient in enumerate(self.filtered_ingredients):
            var = tk.BooleanVar(value=False)
            self.ingredient_vars[ingredient] = var

            cb = ttk.Checkbutton(self.scrollable_frame, text=ingredient.capitalize(),
                                 variable=var, command=self.update_selected_list,
                                 style='Ingredient.TCheckbutton')
            cb.grid(row=i, column=0, sticky=tk.W, pady=2, padx=5)
            self.ingredient_checkboxes.append(cb)

    def filter_ingredients(self, event=None):
        """Фильтрует ингредиенты по поисковому запросу"""
        search_term = self.search_var.get().lower()

        if not search_term:
            self.filtered_ingredients = self.available_ingredients.copy()
        else:
            self.filtered_ingredients = [
                ing for ing in self.available_ingredients
                if search_term in ing.lower()
            ]

        self.create_ingredient_checkboxes()

    def update_selected_list(self):
        """Обновляем список выбранных ингредиентов"""
        self.selected_ingredients = []
        self.selected_listbox.delete(0, tk.END)

        for ingredient, var in self.ingredient_vars.items():
            if var.get() and ingredient in self.filtered_ingredients:
                self.selected_ingredients.append(ingredient)
                self.selected_listbox.insert(tk.END, f"• {ingredient.capitalize()}")

    def select_all_ingredients(self):
        """Выбирает все ингредиенты"""
        for ingredient in self.filtered_ingredients:
            if ingredient in self.ingredient_vars:
                self.ingredient_vars[ingredient].set(True)

        self.update_selected_list()

    def clear_all_ingredients(self):
        """Очищает все выбранные ингредиенты"""
        for var in self.ingredient_vars.values():
            var.set(False)

        self.selected_ingredients = []
        self.selected_listbox.delete(0, tk.END)
        self.results_tree.delete(*self.results_tree.get_children())

    def find_recipes(self):
        """Ищем рецепты по выбранным ингредиентам"""
        # Очищаем предыдущие результаты
        self.results_tree.delete(*self.results_tree.get_children())

        if not self.selected_ingredients:
            messagebox.showinfo("Информация", "Пожалуйста, выберите хотя бы один ингредиент")
            return

        # Ищем подходящие рецепты
        matching_recipes = []

        for recipe in self.recipes:
            # Преобразуем ингредиенты рецепта в нижний регистр для сравнения
            recipe_ingredients = [ing.lower() for ing in recipe["ingredients"]]

            # Проверяем, есть ли все выбранные ингредиенты в рецепте
            match = all(ing in recipe_ingredients for ing in self.selected_ingredients)

            if match:
                matching_recipes.append(recipe)

        if not matching_recipes:
            messagebox.showinfo("Результат",
                                "По выбранным ингредиентам рецептов не найдено. Попробуйте выбрать меньше ингредиентов.")
            return

        # Сортируем рецепты по сложности и времени
        difficulty_order = {"очень легко": 0, "легко": 1, "средне": 2, "сложно": 3}
        matching_recipes.sort(key=lambda r: (difficulty_order.get(r.get("difficulty", "средне"), 2),
                                             len(r["ingredients"])))

        # Отображаем результаты
        for recipe in matching_recipes:
            self.results_tree.insert("", tk.END,
                                     values=(recipe["name"],
                                             recipe["cooking_time"],
                                             recipe.get("difficulty", "не указано"),
                                             recipe.get("category", "не указано")),
                                     tags=("recipe",))

        # Обновляем статистику
        self.stats_label.config(
            text=f"Всего рецептов: {len(self.recipes)} | Ингредиентов: {len(self.available_ingredients)} | Найдено: {len(matching_recipes)}")

    def show_recipe_details(self, event):
        """Показываем детали выбранного рецепта"""
        selection = self.results_tree.selection()
        if not selection:
            return

        # Получаем выбранный рецепт
        item = self.results_tree.item(selection[0])
        recipe_name = item["values"][0]

        # Находим рецепт в базе данных
        recipe = None
        for r in self.recipes:
            if r["name"] == recipe_name:
                recipe = r
                break

        if not recipe:
            return

        # Создаем окно с деталями рецепта
        detail_window = tk.Toplevel(self.root)
        detail_window.title(f"📖 Рецепт: {recipe['name']}")
        detail_window.geometry("800x700")
        detail_window.configure(bg='white')

        # Основной фрейм с прокруткой
        main_frame = ttk.Frame(detail_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=760)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовок рецепта
        title_label = ttk.Label(scrollable_frame, text=recipe["name"],
                                font=("Arial", 16, "bold"), background='white')
        title_label.pack(pady=(10, 5))

        # Информация о рецепте
        info_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        info_frame.pack(fill="x", padx=10, pady=5)

        info_text = f"⏱ Время приготовления: {recipe['cooking_time']} | " \
                    f"📊 Сложность: {recipe.get('difficulty', 'не указано')} | " \
                    f"🏷️ Категория: {recipe.get('category', 'не указано')}"

        info_label = ttk.Label(info_frame, text=info_text, background='white',
                               font=("Arial", 10))
        info_label.pack(pady=5)

        # Ингредиенты
        ingredients_frame = ttk.LabelFrame(scrollable_frame, text="🛒 Ингредиенты", padding="15")
        ingredients_frame.pack(fill="x", padx=10, pady=10)

        ingredients_text = "\n".join([f"• {ing.capitalize()}" for ing in recipe["ingredients"]])
        ingredients_display = scrolledtext.ScrolledText(ingredients_frame,
                                                        height=min(10, len(recipe["ingredients"])),
                                                        width=70,
                                                        font=("Arial", 10),
                                                        wrap=tk.WORD,
                                                        bg='white',
                                                        relief='flat')
        ingredients_display.insert(1.0, ingredients_text)
        ingredients_display.config(state="disabled")
        ingredients_display.pack(fill="both", expand=True)

        # Инструкция приготовления
        instructions_frame = ttk.LabelFrame(scrollable_frame, text="👨‍🍳 Полное описание приготовления", padding="15")
        instructions_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        instructions_display = scrolledtext.ScrolledText(instructions_frame,
                                                         height=20,
                                                         width=70,
                                                         font=("Arial", 10),
                                                         wrap=tk.WORD,
                                                         bg='white',
                                                         relief='flat')
        instructions_display.insert(1.0, recipe["instructions"])
        instructions_display.config(state="disabled")
        instructions_display.pack(fill="both", expand=True)

        # Кнопка закрытия
        close_button = ttk.Button(scrollable_frame, text="Закрыть",
                                  command=detail_window.destroy)
        close_button.pack(pady=(10, 5))

    def add_recipe(self):
        """Добавляем новый рецепт"""
        add_window = tk.Toplevel(self.root)
        add_window.title("➕ Добавить новый рецепт")
        add_window.geometry("600x700")

        # Основной фрейм с прокруткой
        main_frame = ttk.Frame(add_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Canvas для прокрутки
        canvas = tk.Canvas(main_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Card.TFrame')

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=560)
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Заголовок
        title_label = ttk.Label(scrollable_frame, text="Добавление нового рецепта",
                                font=("Arial", 14, "bold"), background='white')
        title_label.pack(pady=(10, 15))

        # Поля формы
        fields_frame = ttk.Frame(scrollable_frame, style='Card.TFrame')
        fields_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Название рецепта
        ttk.Label(fields_frame, text="Название рецепта:", background='white').grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(fields_frame, width=40)
        name_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))

        # Категория
        ttk.Label(fields_frame, text="Категория:", background='white').grid(row=1, column=0, sticky=tk.W, pady=5)
        category_entry = ttk.Combobox(fields_frame,
                                      values=["завтрак", "обед", "ужин", "салат", "суп", "десерт", "закуска",
                                              "напиток"], width=37)
        category_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        category_entry.set("обед")

        # Сложность
        ttk.Label(fields_frame, text="Сложность:", background='white').grid(row=2, column=0, sticky=tk.W, pady=5)
        difficulty_entry = ttk.Combobox(fields_frame, values=["очень легко", "легко", "средне", "сложно"], width=37)
        difficulty_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        difficulty_entry.set("средне")

        # Время приготовления
        ttk.Label(fields_frame, text="Время приготовления:", background='white').grid(row=3, column=0, sticky=tk.W,
                                                                                      pady=5)
        time_entry = ttk.Entry(fields_frame, width=40)
        time_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=(10, 0))
        time_entry.insert(0, "30 минут")

        # Ингредиенты
        ttk.Label(fields_frame, text="Ингредиенты (через запятую):", background='white').grid(row=4, column=0,
                                                                                              sticky=tk.NW, pady=5)
        ingredients_text = tk.Text(fields_frame, height=6, width=30)
        ingredients_text.grid(row=4, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))

        # Инструкция
        ttk.Label(fields_frame, text="Полное описание приготовления:", background='white').grid(row=5, column=0,
                                                                                                sticky=tk.NW, pady=5)
        instructions_text = tk.Text(fields_frame, height=12, width=30)
        instructions_text.grid(row=5, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5, padx=(10, 0))

        # Подсказка для инструкции
        ttk.Label(fields_frame, text="Опишите подробно все шаги приготовления",
                  font=("Arial", 8), foreground="gray", background='white').grid(row=6, column=1, sticky=tk.W,
                                                                                 pady=(0, 10), padx=(10, 0))

        # Кнопки
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=20)

        def save_recipe():
            name = name_entry.get().strip()
            ingredients = [ing.strip() for ing in ingredients_text.get(1.0, tk.END).strip().split(",") if ing.strip()]
            instructions = instructions_text.get(1.0, tk.END).strip()
            cooking_time = time_entry.get().strip()
            difficulty = difficulty_entry.get().strip()
            category = category_entry.get().strip()

            if not name or not ingredients or not instructions or not cooking_time:
                messagebox.showerror("Ошибка", "Пожалуйста, заполните все обязательные поля")
                return

            # Создаем новый рецепт
            new_recipe = {
                "name": name,
                "ingredients": ingredients,
                "instructions": instructions,
                "cooking_time": cooking_time,
                "difficulty": difficulty,
                "category": category
            }

            # Добавляем в базу данных
            self.recipes.append(new_recipe)
            self.save_recipes()

            # Обновляем список ингредиентов
            self.extract_ingredients()

            # Обновляем интерфейс
            self.filter_ingredients()
            self.update_selected_list()
            self.stats_label.config(
                text=f"Всего рецептов: {len(self.recipes)} | Ингредиентов: {len(self.available_ingredients)}")

            messagebox.showinfo("Успех", "Рецепт успешно добавлен!")
            add_window.destroy()

        def cancel():
            add_window.destroy()

        ttk.Button(button_frame, text="Сохранить рецепт", command=save_recipe, width=20).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Отмена", command=cancel, width=20).grid(row=0, column=1, padx=5)

        # Настройка веса для растягивания
        fields_frame.columnconfigure(1, weight=1)
        fields_frame.rowconfigure(4, weight=1)
        fields_frame.rowconfigure(5, weight=2)


def main():
    root = tk.Tk()
    app = RecipeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()