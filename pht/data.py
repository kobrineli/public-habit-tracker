from pht.utils import gen_keyboard


class Texts:
    main_menu_text = "👋 Привет, ты в главном меню"
    my_habits_button = "🦾 Мои привычки"
    add_habit_button = "➕ Добавить привычку"
    rating_button = "🏆 Рейтинг"
    change_past_button = "⏪ Изменить прошлое"
    settings_button = "⚙️ Настройки"
    question_button = "❓ Что делать?"
    back_button = "⬅️  Назад"
    onboarding_1_text = (
        "🦾 Я создан для *отслеживания твоего прогресса по выработке привычек.*"
        "\n\n"
        "✏️ Внеси пару-тройку привычек, которых ты хочешь придерживаться, "
        "укажи периодичность, и каждый вечер я буду спрашивать "
        "тебя, удалось ли тебе преуспеть в каждой из них."
        "\n\n"
        'Например, можно добавить такие привычки: "заниматься спортом _2 раза в неделю_", '
        '"читать по 20 минут _каждый день_", '
        '"_2 раза в неделю_ гулять по часу на природе". Как видишь, периодичность задаётся очень гибко.'
        "\n\n"
        "🏆 Моя фишка — **публичный рейтинг привычек**. Он подталкивает всех участников не лениться "
        "и придерживаться привычек, которые для них важны. Если хочешь, можешь не участвовать в нём, это опционально."
    )

    onboarding_2_text = "<Продолжение анбординга>"
    onboarding_1_next_button = "👀 Интересно"
    onboarding_2_next_button = "🤩 Я в деле"
    welcome_back = "Рад снова тебя видеть! Раз уж ты нажал /start, запускаю анбординг.."
    invalid_input = "Здесь нужно нажать на одну из кнопок"

    @staticmethod
    def my_habits_text(habits: ...):
        header = "*Твои привычки:*"
        habits = [
            "- *Заниматься спортом*: два раза в неделю",
            "- *Не есть сладкое после ужина*: каждый день",
        ]
        return header + "\n\n" + "\n".join(habits)


class Keyboards:
    menu = gen_keyboard(
        [
            [Texts.my_habits_button, Texts.rating_button],
            [Texts.question_button, Texts.settings_button],
        ]
    )

    onboarding_1 = gen_keyboard([[Texts.onboarding_1_next_button]])
    onboarding_2 = gen_keyboard([[Texts.onboarding_2_next_button]])

    my_habits = gen_keyboard(
        [[Texts.add_habit_button], [Texts.change_past_button], [Texts.back_button]]
    )

    back = gen_keyboard([[Texts.back_button]])


class States:
    my_habits = "my_habits"
