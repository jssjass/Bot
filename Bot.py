class RegistrationState:
    """Абстрактное состояние чат-бота"""
    def handle(self, bot, message):
        """Обрабатывает сообщение и возвращает следующее состояние"""
        raise NotImplementedError("Метод handle() должен быть переопределен в подклассе")


class MainMenuState(RegistrationState):
    """Состояние главного меню"""
    def handle(self, bot, message):
        if not message.strip():
            # Пустое сообщение: показать главное меню
            return self.show_menu()
        else:
            # Обработка выбора пользователя
            option = message.strip()
            return self.process_option(bot, option)

    def show_menu(self):
        response = (
            "Главное меню:\n"
            "1. Зарегистрироваться на рейс\n"
            "2. Просмотреть регистрации\n"
            "3. Отменить регистрацию\n"
            "4. Выйти\n"
            "Выберите опцию (1-4):"
        )
        return response, self

    def process_option(self, bot, option):
        if option == "1":
            response = "Введите имя пассажира:"
            return response, AskNameState()
        elif option == "2":
            if bot.registrations:
                registration_list = "\n".join(
                    [f"{name}: Рейс {flight}" for name, flight in bot.registrations.items()]
                )
                response = f"Текущие регистрации:\n{registration_list}"
            else:
                response = "Нет существующих регистраций."
            response += (
                "\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, self
        elif option == "3":
            response = "Введите имя пассажира для отмены регистрации:"
            return response, CancelRegistrationStartState()
        elif option == "4":
            response = "Завершение работы."
            return response, EndState()
        else:
            response = "Неверный ввод. Пожалуйста, выберите опцию от 1 до 4."
            return response, self


class AskNameState(RegistrationState):
    """Состояние запроса имени пассажира"""
    def handle(self, bot, message):
        name = message.strip()
        if name:
            bot.current_name = name
            response = f"Укажите номер рейса для пассажира {name}:"
            return response, AskFlightNumberState()
        else:
            response = "Имя не может быть пустым. Пожалуйста, введите корректное имя пассажира:"
            return response, self


class AskFlightNumberState(RegistrationState):
    """Состояние запроса номера рейса"""
    def handle(self, bot, message):
        flight_number = message.strip()
        if flight_number:
            bot.current_flight = flight_number
            response = (
                f"Подтвердите регистрацию на рейс {flight_number} на имя пассажира {bot.current_name}? (да/нет)"
            )
            return response, ConfirmationState()
        else:
            response = f"Номер рейса не может быть пустым. Укажите номер рейса для пассажира {bot.current_name}:"
            return response, self


class ConfirmationState(RegistrationState):
    """Состояние подтверждения регистрации"""
    def handle(self, bot, message):
        answer = message.strip().lower()
        if answer == "да":
            bot.registrations[bot.current_name] = bot.current_flight
            response = (
                "Регистрация успешно завершена!\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, MainMenuState()
        elif answer == "нет":
            response = (
                "Регистрация отменена.\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, MainMenuState()
        else:
            response = "Пожалуйста, ответьте 'да' или 'нет':"
            return response, self


class CancelRegistrationStartState(RegistrationState):
    """Состояние запроса имени пассажира для отмены регистрации"""
    def handle(self, bot, message):
        name = message.strip()
        if name in bot.registrations:
            bot.current_name = name
            response = f"Вы уверены, что хотите отменить регистрацию для {name}? (да/нет)"
            return response, CancelConfirmationState()
        else:
            response = (
                "Пассажир с таким именем не найден.\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, MainMenuState()


class CancelConfirmationState(RegistrationState):
    """Состояние подтверждения отмены регистрации"""
    def handle(self, bot, message):
        answer = message.strip().lower()
        if answer == "да":
            del bot.registrations[bot.current_name]
            response = (
                "Регистрация успешно отменена.\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, MainMenuState()
        elif answer == "нет":
            response = (
                "Отмена не выполнена.\n\nГлавное меню:\n"
                "1. Зарегистрироваться на рейс\n"
                "2. Просмотреть регистрации\n"
                "3. Отменить регистрацию\n"
                "4. Выйти\n"
                "Выберите опцию (1-4):"
            )
            return response, MainMenuState()
        else:
            response = "Пожалуйста, ответьте 'да' или 'нет':"
            return response, self


class EndState(RegistrationState):
    """Состояние завершения работы бота"""
    def handle(self, bot, message):
        return "Чат-бот завершил работу.", self


class RegistrationBot:
    """Чат-бот для регистрации на авиарейс с использованием FSM"""

    def __init__(self):
        self.state = MainMenuState()
        self.registrations = {}  # Хранение регистраций в виде {имя: номер рейса}
        self.current_name = ""
        self.current_flight = ""

    def process_message(self, message):
        """Обрабатывает сообщение пользователя и обновляет состояние"""
        response, next_state = self.state.handle(self, message)
        self.state = next_state
        return response


def main():
    """Запускает чат-бота в консоли"""
    bot = RegistrationBot()
    print("Бот: ", bot.process_message(""))  # Инициализация и отображение главного меню

    while not isinstance(bot.state, EndState):
        message = input("Вы: ")
        response = bot.process_message(message)
        print("Бот: ", response)

    print("Бот завершил работу.")


if __name__ == "__main__":
    main()
