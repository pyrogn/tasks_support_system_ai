import pandas as pd
from ollama import Client

# Инициализация клиента Ollama
client = Client()

# Функция для обработки текста через LLM
# llama3.1 - отказывается отвечать
# phi3.5 (3.8b) - неточный
# mistral-nemo (12b) долгий, привирает
# qwen2.5 (7b) - лучший
# gemma2:9b - лучший
def process_text(system_prompt, user_input):
    response = client.chat(model='gemma2:9b', messages=[
        {
            'role': 'system',
            'content': system_prompt
        },
        {
            'role': 'user',
            'content': user_input
        }
    ])
    return response['message']['content']

# df = pd.read_csv('your_data.csv')

base_system_prompt = """
Вы - система для переписывания текста с сохранением конфиденциальности. Ваша задача - переписать входной текст пользователя, заменяя конфиденциальную информацию соответствующими плейсхолдерами. Следуйте этим правилам:

- Замените номера телефонов на [ТЕЛЕФОН]
- Замените имена на [ИМЯ]
- Замените адреса электронной почты на [EMAIL]
- Замените физические адреса на [АДРЕС]
- Замените даты на [ДАТА]
- Замените названия компаний на [КОМПАНИЯ]
- Замените должности на [ДОЛЖНОСТЬ]
- Замените названия продуктов на [ПРОДУКТ]
- Замените номера счетов на [СЧЕТ]
- Замените любую другую идентифицирующую информацию на [ЛИЧНЫЕ_ДАННЫЕ]

Сохраняйте общую структуру и контекст сообщения, анонимизируя при этом личную информацию. Используйте соответствующие плейсхолдеры последовательно на протяжении всего текста.
Важно: ответь только отредактированным предложением, без дополнительной информации.
"""

# # Обработка всех строк
# df['processed_text'] = df['original_text'].apply(lambda x: process_text(base_system_prompt, x))

# # Сохранение результатов
# df.to_csv('processed_data.csv', index=False)

# Экспериментирование с системным промптом
def experiment_with_prompt(original_text, system_prompt):
    processed_text = process_text(system_prompt, original_text)
    print(f"Оригинальный текст:\n{original_text}\n")
    print(f"Обработанный текст:\n{processed_text}\n")
    print("=" * 50)

# Пример использования
sample_text = "Добрый день. Прошу рассмотреть инцидент по Семье здесь: Тарификационный номер 31231231231 Номера членов семьи: +31231231231 +31231231231 +31231231231   Добавленные члены семьи исчезли, добавить их заново не дает. Обновление приложения и новая установка приложения никак не изменило ситуацию. Клиент проживает в г. Минск, ул. Анекдотов, д.13 кв.28. Клиент работает в ООО Мыши и коровы, его график работы 9-18. Ездит на электричке по ул. Малышева по субботам. Вступил в клуб Анонимные Алкоголики Мытищи. Является председателем комитета Любителей Фильмов Без Сюжетных Переворотов с 1 июля 2012 года.  У клиента оформлена подписка 3923848 по услуге Автоответчик. Услуга «технологическая трекинг семья здесь» на номерах есть.   С уважением,  Иван Иванов Специалист по маркетингу  Отдел базовых сервисов и бизнес-пр"
experiment_with_prompt(sample_text, base_system_prompt)

modified_prompt = base_system_prompt + "\nНе меняй нигде грамматику, только заменяй отдельные части. Убирай информацию, которая может указать на человека лично. Общую информацию стоит оставлять."
experiment_with_prompt(sample_text, modified_prompt)
