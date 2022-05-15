import json


def load(lang):
    return json.load(open(f"./lang/{lang}.json", "r"))





def language(func: Callable) -> Callable:
    async def decorator(client, obj: Union[Message, int, Update], *args):
        try:
            if isinstance(obj, int):
                chat_id = obj
            elif isinstance(obj, Message):
                chat_id = obj.chat.id
            elif isinstance(obj, Update):
                chat_id = obj.chat_id
            group_lang = get_group(chat_id)["lang"]
        except BaseException:
            group_lang = config.LANGUAGE
        lang = load(group_lang)
        return await func(client, obj, lang)

    return decorator
