class RegistrationState:
    """Состояния автомата для регистрации на рейс и взаимодействия с меню"""
    MAIN_MENU = "main_menu"
    REGISTER_FLIGHT_START = "register_flight_start"
    ASK_NAME = "ask_name"
    ASK_FLIGHT_NUMBER = "ask_flight_number"
    CONFIRMATION = "confirmation"
    VIEW_REGISTRATIONS = "view_registrations"
    CANCEL_REGISTRATION_START = "cancel_registration_start"
    CANCEL_CONFIRMATION = "cancel_confirmation"
    END = "end"

class RegistrationBot:
    """Расширенный чат-бот для регистрации на авиарейс с поддержкой меню"""

    def __init__(self):
        self.state = RegistrationState.MAIN_MENU
        self.registrations = {}  # Хранение регистраций в виде {имя: номер рейса}
        self.current_name = ""
        self.current_flight = ""

    def process_message(self, message):
        """Обрабатывает сообщение пользователя и генерирует ответ в зависимости от состояния"""

        if self.state == RegistrationState.MAIN_MENU:
            if not message.strip():
                # Если сообщение пустое, просто вывести главное меню
                response = (
                    "Главное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
            else:
                # Обработка выбора пользователя
                if message == "1":
                    response = "Введите имя пассажира:"
                    self.state = RegistrationState.ASK_NAME
                elif message == "2":
                    if self.registrations:
                        response = "Текущие регистрации:\n" + "\n".join(
                            [f"{name}: Рейс {flight}" for name, flight in self.registrations.items()]
                        )
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
                elif message == "3":
                    response = "Введите имя пассажира для отмены регистрации:"
                    self.state = RegistrationState.CANCEL_REGISTRATION_START
                elif message == "4":
                    response = "Завершение работы."
                    self.state = RegistrationState.END
                else:
                    response = "Неверный ввод. Пожалуйста, выберите опцию от 1 до 4."
            return response

        elif self.state == RegistrationState.ASK_NAME:
            self.current_name = message.strip()
            if self.current_name:
                response = f"Укажите номер рейса для пассажира {self.current_name}:"
                self.state = RegistrationState.ASK_FLIGHT_NUMBER
            else:
                response = "Имя не может быть пустым. Пожалуйста, введите корректное имя пассажира:"
            return response

        elif self.state == RegistrationState.ASK_FLIGHT_NUMBER:
            self.current_flight = message.strip()
            if self.current_flight:
                response = (
                    f"Подтвердите регистрацию на рейс {self.current_flight} на имя пассажира {self.current_name}? (да/нет)"
                )
                self.state = RegistrationState.CONFIRMATION
            else:
                response = f"Номер рейса не может быть пустым. Укажите номер рейса для пассажира {self.current_name}:"
            return response

        elif self.state == RegistrationState.CONFIRMATION:
            if message.lower() == "да":
                self.registrations[self.current_name] = self.current_flight
                response = (
                    "Регистрация успешно завершена!\n\nГлавное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
                self.state = RegistrationState.MAIN_MENU
            elif message.lower() == "нет":
                response = (
                    "Регистрация отменена.\n\nГлавное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
                self.state = RegistrationState.MAIN_MENU
            else:
                response = "Пожалуйста, ответьте 'да' или 'нет':"
            return response

        elif self.state == RegistrationState.CANCEL_REGISTRATION_START:
            self.current_name = message.strip()
            if self.current_name in self.registrations:
                response = f"Вы уверены, что хотите отменить регистрацию для {self.current_name}? (да/нет)"
                self.state = RegistrationState.CANCEL_CONFIRMATION
            else:
                response = (
                    "Пассажир с таким именем не найден.\n\nГлавное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
                self.state = RegistrationState.MAIN_MENU
            return response

        elif self.state == RegistrationState.CANCEL_CONFIRMATION:
            if message.lower() == "да":
                del self.registrations[self.current_name]
                response = (
                    "Регистрация успешно отменена.\n\nГлавное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
                self.state = RegistrationState.MAIN_MENU
            elif message.lower() == "нет":
                response = (
                    "Отмена не выполнена.\n\nГлавное меню:\n"
                    "1. Зарегистрироваться на рейс\n"
                    "2. Просмотреть регистрации\n"
                    "3. Отменить регистрацию\n"
                    "4. Выйти\n"
                    "Выберите опцию (1-4):"
                )
                self.state = RegistrationState.MAIN_MENU
            else:
                response = "Пожалуйста, ответьте 'да' или 'нет':"
            return response

        elif self.state == RegistrationState.END:
            return "Чат-бот завершил работу."

        else:
            self.state = RegistrationState.END
            return "Неизвестное состояние. Завершение работы."

def main():
    """Запускает расширенный чат-бот в консоли"""

    bot = RegistrationBot()
    print("Бот: ", bot.process_message(""))  # Инициализация и отображение главного меню

    while bot.state != RegistrationState.END:
        message = input("Вы: ")
        print("Бот: ", bot.process_message(message))

if __name__ == "__main__":
    main()
