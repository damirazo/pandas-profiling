import warnings
from gettext import translation
from typing import Text, Callable, Optional

# Код языка локализации по умолчанию
DEFAULT_LANG_CODE = 'en'
LC_MESSAGES = 'messages'


def auto_activator(method: Callable):
    """
    Декоратор для автоматической активации реестра дефолтными настройками,
    если ручной активации не было выполнено

    :param method: Оборачиваемый метод-дескриптор доступа к значению реестра
    """
    def wrapper(cls: 'LocalizationRegistry', *args, **kwargs):
        if not cls.is_activated:
            cls.activate(DEFAULT_LANG_CODE)

        return method(cls, *args, **kwargs)
    return wrapper


class LocalizationRegistry:
    """
    Реестр для хранения рантаймовой информации
    о текущих настройках локализации приложения
    """
    _code = None
    _trans = None
    _activated = False

    @classmethod
    def activate(
            cls,
            code: Optional[Text] = None,
            locale_dir: Optional[Text] = None):
        """
        Инициализация реестра указанным кодом локализации

        :param code: Код локализации
        :param locale_dir: Путь до директории с файлами локализации
        """
        cls._code = code or DEFAULT_LANG_CODE
        cls._trans = translation(
            domain=LC_MESSAGES,
            localedir=locale_dir,
            languages=(code,))
        cls._activated = True

    @classmethod
    def is_activated(cls) -> bool:
        """Признак проведенной активации реестра"""
        return cls._activated

    @classmethod
    def get_code(cls) -> Text:
        """Дескриптор для доступа к коду локализации"""
        return cls._code

    @classmethod
    def get_translation(cls):
        """Дескриптор для доступа к объекту локализации"""
        return cls._trans


def gettext(message: Text) -> Text:
    """
    Обертка над GNU gettext

    Выполняет перевод указанной строки
    при активизированных настройках локализации
    """
    eol_message = message.replace('\r\n', '\n').replace('\r', '\n')

    if eol_message:
        translation_object = LocalizationRegistry.get_translation()
        result = translation_object.gettext(eol_message)
    else:
        # Return an empty value of the corresponding type if an empty message
        # is given, instead of metadata, which is the default gettext behavior.
        result = type(message)('')

    return result
