# All rights for this file belong to Fyodor Doletov <doletov.fyodor@yandex.ru>. Do NOT edit these comments
# You can copy this file, modify it (but don't edit these comments) and use in your own project for free

import traceback
from threading import Thread


class BotsRunner:

    def __init__(self, admins=tuple(), retries=0, show_traceback=False):
        self.__bots = dict()
        self.__bots_status = dict()
        self.__main_bot = None
        self.__admins = list(admins)
        self.__retries = retries
        self.__show_traceback = show_traceback

    def format_status(self):
        text = "Статус работы ботов:\n\n"
        for botname in self.__bots_status:
            if self.__bots_status[botname]:
                text += "✅ " + botname + " - Online!\n"
            else:
                text += "❌ " + botname + " - Offline!\n"
        return text

    def get_status(self):
        return dict(self.__bots_status)

    def add_bots(self, bot_dict):
        for botname in bot_dict:
            self.add_bot(botname, bot_dict[botname])

    def add_bot(self, name, bot):
        if name in self.__bots:
            raise NotANewBotException()
        self.__bots[name] = bot
        self.__bots_status[name] = False

    def set_main_bot(self, bot):
        self.__main_bot = bot

    def run(self):
        for botname in self.__bots:
            if not self.__bots_status[botname]:
                Thread(target=self.__poll, args=[botname]).start()

    def __warn_about_fail(self, botname):
        if self.__main_bot is None:
            return
        text = "Бот " + botname + " отвалился!\n\n"
        text += self.format_status() + "\n\n"
        if self.__show_traceback:
            text += "<code>" + traceback.format_exc() + "</code>"
        for adm in self.__admins:
            self.__main_bot.send_message(adm, text, parse_mode="HTML")

    def __tell_about_restart(self, botname, local_retries):
        if self.__main_bot is None:
            return
        for adm in self.__admins:
            self.__main_bot.send_message(
                adm,
                "♻️ Рестарт бота " + botname +
                ". Осталось " + local_retries + " падений до необходимости рестарта приложения"
            )

    def __poll(self, botname):
        local_retries = self.__retries
        while True:
            try:
                self.__bots_status[botname] = True
                self.__bots[botname].polling(none_stop=True, timeout=600)
            except Exception:
                self.__bots_status[botname] = False
                self.__warn_about_fail(botname)
                if local_retries > 0:
                    local_retries -= 1
                    self.__tell_about_restart(botname, local_retries)
                    continue
                break


class NotANewBotException(Exception):

    def __init__(self):
        Exception.__init__(self, "Bot is already in list!")
