from jinja2 import Environment, FileSystemLoader


def render(template_name, **kwargs):
    """
    Минимальный пример работы с шаблонизатором
    :param template_name: имя шаблона
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # Открываем шаблон по имени
    with open(template_name, encoding='utf-8') as f:
        # Читаем
        template_str = f.read()
    template = Environment(loader=FileSystemLoader("templates/")).from_string(template_str)
    return template.render(default_start_page_lanes=template,
                           **kwargs)