# Telegram Бот — Запись на пробное занятие по английскому

Этот Telegram-бот — виртуальный администратор школы английского языка. Он помогает пользователю быстро и удобно записаться на пробный урок, собирая нужную информацию через последовательный диалог.

## 🔍 Функциональность

- Стартовое приветствие с кнопкой действия
- Последовательное анкетирование:
  - Цель изучения английского
  - Уровень языка
  - Возраст
  - Предпочтения по преподавателю
  - Удобный формат (онлайн/офлайн)
  - Предпочтительное время
- Подведение итогов и отправка анкеты пользователю
- Поддержка FSM (Finite State Machine) для управления шагами диалога

## 🧠 Используемые технологии

- Python 3.10+
- [aiogram](https://github.com/aiogram/aiogram) — асинхронный Telegram Bot API framework
- FSM из `aiogram` для пошагового взаимодействия
- `MemoryStorage` для хранения состояний в памяти
