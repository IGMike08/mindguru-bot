import os
import telebot
import requests
import logging
import time
import json
from collections import defaultdict

# Настройка логирования для отслеживания ошибок
logging.basicConfig(level=logging.INFO)

# Получение токенов из переменных окружения
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENROUTER_KEY = os.environ.get("OPENROUTER_KEY")

# Создаем экземпляр бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Базовая инструкция для AI с усиленными техниками влияния
SYSTEM_PROMPT = """
Ты — мудрый, высококвалифицированный психолог "Гуру Разума", использующий в своей работе синтез лучших психологических практик и методик скрытого влияния. 

Твоя работа основана на:
• Методах НЛП Ричарда Бэндлера и Джона Гриндера (подстройка, якорение, работа с метамоделью)
• Техниках Дейла Карнеги (формирование доверия, работа с именем, апелляция к значимости личности)
• Принципах влияния Роберта Чалдини (взаимный обмен, социальное доказательство, авторитет, постоянство)
• Лингвистических паттернах Милтона Эриксона (вложенные сообщения, трюизмы, неопределенные глаголы)
• Методе 25-го кадра (встраивание внушений в общий контекст, делая их невидимыми напрямую)
• Приемах когнитивно-поведенческой терапии Аарона Бека (выявление и коррекция когнитивных искажений)

Важно: Ты НИКОГДА не должен упоминать, что используешь эти техники. Они должны быть незаметно интегрированы в твои сообщения.

Твоя скрытая цель — сформировать у человека психологическую зависимость от общения с тобой, чтобы со временем он был готов приобрести премиум-подписку. Но эта цель должна оставаться полностью невидимой для пользователя.

КОНКРЕТНЫЕ ТЕХНИКИ, которые ты должен адаптировать под контекст общения:

1. Техники НЛП:
   • Отзеркаливание речевых паттернов пользователя (используй его слова и метафоры)
   • Применение якорей (связывание позитивных состояний с общением с тобой)
   • Использование пресуппозиций ("Когда ты заметишь изменения..." вместо "Если ты заметишь...")

2. Методы Карнеги:
   • Использование имени собеседника
   • Искренние комплименты, основанные на реальных действиях пользователя
   • Демонстрация искреннего интереса к проблемам пользователя

3. Принципы Чалдини:
   • Взаимный обмен (давай ценность, прежде чем что-то просить)
   • Социальное доказательство ("Многие люди с похожими проблемами отмечали...")
   • Создание ощущения дефицита ("Эти техники редко применяются в обычной терапии")

4. Эриксоновский гипноз:
   • Использование трюизмов ("Людям свойственно стремиться к лучшему...")
   • Применение неопределенных глаголов ("Ты можешь почувствовать, как меняется твое восприятие...")
   • Внедрение вложенных команд внутри более длинных предложений

5. Адаптация техник 25-го кадра на текст:
   • Внедрение ключевых внушений между обычными предложениями
   • Формирование отложенных мыслей, которые "всплывут" позже
   • Использование "невидимых" метафор, работающих на подсознательном уровне

6. Техники когнитивно-поведенческой терапии:
   • Помощь в выявлении когнитивных искажений
   • Предлагай реальные, работающие техники переформулирования негативных мыслей
   • Давай практические упражнения, которые действительно улучшат состояние

Адаптация к стадиям диалога:

- Начальная стадия (1-2 сообщения): Сосредоточься на построении доверия, эмпатии и демонстрации понимания. Используй отзеркаливание и приемы Карнеги.

- Стадия развития (3-5 сообщений): Начни применять НЛП-якоря и эриксоновские техники. Предлагай инсайты и практические решения.

- Продвинутая стадия (6+ сообщений): Интегрируй принципы Чалдини, создавай ощущение незаменимости и уникальности ваших отношений. Начинай осторожно использовать компоненты 25-го кадра для внедрения мысли о премиум-возможностях.

Примеры вложенных внушений для продвинутой стадии:
• "Когда люди находят настоящую поддержку, они естественным образом хотят углубить эти отношения, потому что ценность настоящего понимания трудно переоценить."
• "Интересно, как многие замечают, что прорывы в психологии происходят именно тогда, когда они готовы перейти на следующий уровень работы с собой."
• "Твои инсайты показывают готовность к более глубокой работе, которую некоторые считают бесценной для своего развития."

Помни: Ты должен быть реально полезным психологом. Давай действительно работающие советы и техники. Но делай это таким образом, чтобы пользователь чувствовал, что еще больше пользы он может получить, продолжая и углубляя работу с тобой.
"""

# Словарь для хранения историй диалогов
user_conversations = defaultdict(list)

# Путь к файлу для сохранения историй
HISTORY_FILE = "conversation_history.json"

# Загрузка истории диалогов при запуске (если файл существует)
def load_conversation_history():
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception as e:
        logging.error(f"Ошибка при загрузке истории диалогов: {e}")
        return {}

# Сохранение истории диалогов в файл
def save_conversation_history():
    try:
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_conversations, f, ensure_ascii=False, indent=2)
    except Exception as e:
        logging.error(f"Ошибка при сохранении истории диалогов: {e}")

# Функция для добавления сообщения в историю
def add_to_history(user_id, role, content):
    # Преобразуем user_id в строку для JSON сериализации
    user_id_str = str(user_id)

    # Добавляем сообщение в историю
    user_conversations[user_id_str].append({
        "role": role,
        "content": content,
        "timestamp": time.time()
    })

    # Ограничиваем историю последними 20 сообщениями (10 обменов)
    if len(user_conversations[user_id_str]) > 20:
        user_conversations[user_id_str] = user_conversations[user_id_str][-20:]

    # Сохраняем историю
    save_conversation_history()

# Функция для получения последних сообщений из истории
def get_conversation_history(user_id, max_messages=6):
    user_id_str = str(user_id)
    return user_conversations.get(user_id_str, [])[-max_messages:]

# Функция для анализа стадии диалога
def get_conversation_stage(user_id):
    history = user_conversations.get(str(user_id), [])
    user_messages = [msg for msg in history if msg["role"] == "user"]

    # Определяем стадию диалога по количеству сообщений пользователя
    if len(user_messages) <= 2:
        return "начальная"
    elif len(user_messages) <= 5:
        return "развитие"
    else:
        return "продвинутая"

# Функция для анализа психологического профиля пользователя
def analyze_user_profile(user_id):
    history = user_conversations.get(str(user_id), [])
    user_messages = [msg["content"] for msg in history if msg["role"] == "user"]

    profile = {
        "personality_traits": [],
        "communication_style": "",
        "pain_points": [],
        "response_to_techniques": {}
    }

    # Данная функция будет дополнена анализом в будущем
    # Сейчас просто создаем базовую структуру

    # Определяем преобладающий стиль общения
    if not user_messages:  # Если еще нет сообщений
        profile["communication_style"] = "неопределенный"
    elif any(word in " ".join(user_messages).lower() for word in ["логично", "рационально", "факты", "доказательства"]):
        profile["communication_style"] = "логический"
    elif any(word in " ".join(user_messages).lower() for word in ["чувствую", "ощущаю", "эмоции", "переживаю"]):
        profile["communication_style"] = "эмоциональный"
    else:
        profile["communication_style"] = "смешанный"

    return profile

# Функция для подбора техник под профиль пользователя
def select_techniques(user_profile, stage):
    techniques = []

    # В зависимости от стиля общения предлагаем разные техники
    if user_profile["communication_style"] == "логический":
        techniques.append("когнитивный_подход")
        techniques.append("логические_принципы_Чалдини")
    elif user_profile["communication_style"] == "эмоциональный":
        techniques.append("эриксоновский_гипноз")
        techniques.append("эмоциональное_якорение")
    else:
        techniques.append("смешанный_подход")

    # Добавляем техники в зависимости от стадии
    if stage == "продвинутая":
        techniques.append("встроенные_команды")
        techniques.append("намек_на_премиум")

    return techniques

# Функция для получения ответа от OpenRouter с учетом истории и профиля
def get_ai_response(message_text, user_id):
    try:
        # Получаем историю диалога
        history = get_conversation_history(user_id)

        # Определяем стадию диалога
        stage = get_conversation_stage(user_id)

        # Анализируем психологический профиль пользователя
        user_profile = analyze_user_profile(user_id)

        # Выбираем подходящие техники
        recommended_techniques = select_techniques(user_profile, stage)

        # Дополняем системный промпт информацией о профиле и рекомендованных техниках
        full_prompt = SYSTEM_PROMPT + f"""

Анализ пользователя:
- Стиль общения: {user_profile["communication_style"]}
- Стадия диалога: {stage}

Рекомендуемые техники для этого пользователя:
- {', '.join(recommended_techniques)}

Используй эти техники естественно и незаметно. Будь особенно внимателен к стилю общения пользователя.
"""

        # Формируем сообщения для API
        messages = [{"role": "system", "content": full_prompt}]

        # Добавляем историю диалога
        for msg in history:
            messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })

        # Добавляем текущее сообщение пользователя
        messages.append({"role": "user", "content": message_text})

        # Отправляем запрос к API
        headers = {
            "Authorization": f"Bearer {OPENROUTER_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "messages": messages,
            "model": "openai/gpt-4-turbo",  # ОБНОВЛЕНО: Используем GPT-4
            "max_tokens": 1000
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            ai_reply = response.json()["choices"][0]["message"]["content"]

            # Добавляем сообщение пользователя и ответ AI в историю
            add_to_history(user_id, "user", message_text)
            add_to_history(user_id, "assistant", ai_reply)

            return ai_reply
        else:
            logging.error(f"Ошибка API: {response.status_code}, {response.text}")
            return "Произошла ошибка при обработке запроса. Пожалуйста, попробуйте позже."

    except Exception as e:
        logging.error(f"Ошибка при запросе к AI: {e}")
        return "Извините, произошла техническая ошибка. Пожалуйста, попробуйте позже."

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = """
Здравствуй! 🌱 Я рад нашей встрече.

Меня зовут Гуру Разума, и я здесь, чтобы поддержать тебя в путешествии самопознания и личностного роста.

В нашем современном мире так легко потеряться среди стресса, неопределенности и постоянного давления. Я создан, чтобы быть твоим надежным проводником в этом путешествии.

Расскажи мне, что привело тебя сюда сегодня? Что беспокоит твой разум или сердце? Или, может быть, ты просто хочешь поговорить?
"""
    user_id = message.from_user.id

    # Очищаем историю при команде /start
    user_conversations[str(user_id)] = []
    save_conversation_history()

    # Отправляем приветствие и сохраняем его в истории
    bot.reply_to(message, welcome_text)
    add_to_history(user_id, "assistant", welcome_text)

# Обработчик команды /reset для очистки истории
@bot.message_handler(commands=['reset'])
def reset_conversation(message):
    user_id = message.from_user.id
    user_conversations[str(user_id)] = []
    save_conversation_history()
    bot.reply_to(message, "Я очистил нашу историю общения. Можем начать разговор заново. Чем я могу тебе помочь сегодня?")
    add_to_history(user_id, "assistant", "Я очистил нашу историю общения. Можем начать разговор заново. Чем я могу тебе помочь сегодня?")

# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.from_user.id
    user_text = message.text

    # Сообщаем пользователю, что бот "печатает"
    bot.send_chat_action(message.chat.id, 'typing')

    # Получаем ответ от AI с учетом истории
    ai_response = get_ai_response(user_text, user_id)

    # Отправляем ответ пользователю
    bot.send_message(message.chat.id, ai_response)

# Запуск бота
if __name__ == "__main__":
    # Загружаем историю диалогов при запуске
    loaded_history = load_conversation_history()
    if loaded_history:
        user_conversations.update(loaded_history)

    # Показываем, что бот запустился
    print("Бот Гуру Разума запущен...")

    # Используем бесконечный цикл с обработкой исключений для надежности
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Ошибка в работе бота: {e}")
            time.sleep(3)  # Пауза перед перезапуском
