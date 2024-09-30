class RegistrationState:
  """Состояния автомата для регистрации на рейс"""
  START = "start"
  ASK_NAME = "ask_name"
  ASK_FLIGHT_NUMBER = "ask_flight_number"
  CONFIRMATION = "confirmation"
  END = "end"

class RegistrationBot:
  """Простой чат-бот для регистрации на авиарейс"""

  def __init__(self):
    self.state = RegistrationState.START

  def process_message(self, message):
    """Обрабатывает сообщение пользователя и генерирует ответ"""

    if self.state == RegistrationState.START:
      response = "Введите имя пассажира"
      self.state = RegistrationState.ASK_NAME
    elif self.state == RegistrationState.ASK_NAME:
      self.passenger_name = message
      response = f"Укажите номер рейса для пассажира {self.passenger_name}:"
      self.state = RegistrationState.ASK_FLIGHT_NUMBER
    elif self.state == RegistrationState.ASK_FLIGHT_NUMBER:
      self.flight_number = message
      response = f"Подтвердите регистрацию на рейс {self.flight_number} на имя пассажира {self.passenger_name}? (да/нет)"
      self.state = RegistrationState.CONFIRMATION
    elif self.state == RegistrationState.CONFIRMATION:
      if message.lower() == "да":
        response = "Регистрация успешно завершена!"
      else:
        response = "Регистрация отменена."
      self.state = RegistrationState.END
    else:
      response = "Завершение работы."

    return response

def main():
  """Запускает чат-бота в консоли"""

  bot = RegistrationBot()
  print("Бот: ", bot.process_message(""))

  while bot.state != RegistrationState.END:
    message = input("Вы: ")
    print("Бот: ", bot.process_message(message))

if __name__ == "__main__":
  main()
