from nonebot.adapters.telegram import Bot


@Bot.on_called_api
async def _(bot: Bot, exception: Exception, api: str, data: dict, result):
    if str(data.get("chat_id")) not in bot.config.superusers:
        for chat_id in bot.config.superusers:
            await bot.send_message(
                chat_id=chat_id,
                text=f"CalledApi: {api}\n" + str(result),
            )
