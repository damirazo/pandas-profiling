"""Contains all templates used for generating the HTML profile report"""
import jinja2
from jinja2 import Environment, PackageLoader

from pandas_profiling import LocalizationRegistry
from pandas_profiling.report.formatters import (
    fmt_percent,
    fmt_bytesize,
    fmt_numeric,
    fmt_array,
    fmt,
)

# Признак установки объектов локализации для расширения jinja2 i18n
_TRANSLATIONS_INSTALLED = False

# Initializing Jinja
package_loader = PackageLoader(
    "pandas_profiling",
    "report/presentation/flavours/html/templates",
)
jinja2_env = Environment(
    lstrip_blocks=True,
    trim_blocks=True,
    extensions=['jinja2.ext.i18n'],
    loader=package_loader)
jinja2_env.filters["fmt_percent"] = fmt_percent
jinja2_env.filters["fmt_bytesize"] = fmt_bytesize
jinja2_env.filters["fmt_numeric"] = fmt_numeric
jinja2_env.filters["fmt_array"] = fmt_array
jinja2_env.filters["fmt"] = fmt
jinja2_env.filters["dynamic_filter"] = lambda x, v: jinja2_env.filters[v](x)


def url_safe(value):
    """
    Шаблонная функция для замены символов,
    недопустимых к использованию в url в искомой строке
    """
    replaced_symbols = [' ', '(', ')']

    for s in replaced_symbols:
        value = value.replace(s, '')

    return value


jinja2_env.globals.update(url_safe=url_safe)


def template(template_name: str) -> jinja2.Template:
    """Get the template object given the name.

    Args:
      template_name: The name of the template file (.html)

    Returns:
      The jinja2 environment.

    """
    # Установка функции локализации при первом вызове шаблонизатора
    global _TRANSLATIONS_INSTALLED
    if not _TRANSLATIONS_INSTALLED:
        jinja2_env.install_gettext_translations(
            LocalizationRegistry.get_translation())
        _TRANSLATIONS_INSTALLED = True

    return jinja2_env.get_template(template_name)
