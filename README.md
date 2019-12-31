# Manybotslib
 
Fail-safe библиотека для запуска нескольких 
[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) ботов,
использующая модуль threading

(написана для фана, не для серьезных целей)

## Использование

```python
from manybotslib import BotsRunner

# в конструктор можно передать id админов приложения,
# количество попыток перезапуска каждого бота, а так же параметр,
# указывающий, нужно ли отправлять админам полный стектрейс при падении бота
# id нужны для рассылки уведомлений о падении ботов
runner = BotsRunner(admins=(123, 456), retries=2, show_traceback=True)

# класс BotsRunner может принять как одного, так и словарь имен-ботов. Бот должен быть объектом TeleBot
runner.add_bot("Bot1", bot1)
runner.add_bot("Bot2", bot2)

bots = {
    "Bot3", bot3,
    "Bot4", bot4
}
runner.add_bots(bots)

# запуск ботов
runner.run()
```

Добавлять новых ботов можно и после вызова run(), однако после добавления, нужно будет вызвать run() еще раз. Не волнуйтесь, старые боты не перезапустятся

При попытке добавить бота с именем, которое уже есть в списке - получите NotANewBotException

## Падения

При падении одного из ботов, все админы приложения получат уведомление о падении, а так же кол-во оставшихся рестартов бота, и, в зависимости от начальной конфигурации, стектрейс.
Уведомления приходят от "главного" бота, которого необходимо задать. Менять главного бота можно в любое время
в функцию назначения главного бота необходимо передать команду, при получении которой бот будет отправлять админу статус работы всех ботов
Бот не отправит статус, если админы не были назначены либо команду вызвал не админ

**Eсли главного бота не задать, уведомления работать не будут!**

`runner.set_main_bot(admin_bot, 'status')`

## Статус работы ботов

В любой момент можно получить как словарь <string, boolean> о работе ботов, где ключ - имя бота, значение - true, если работает, false, если отключен, обративщись к полю bots_status:

`status = runner.get_status()`

Кроме того, можно получить красиво отформатированную информацию о статусе всех ботов:

`status_text = runner.format_status()`