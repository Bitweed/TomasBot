import configparser
import discord
from discord.ext import tasks

import embed_templates as et


conf = configparser.ConfigParser()
conf.read("settings.ini")

TOKEN: str = conf["Server"]["token"]
SERVER_ID: int = int(conf["Server"]["id"])
chase_status: bool = False

bot = discord.Bot()


@bot.event
async def on_ready():
    print(f"Бот {bot.user} авторизирован!")
    change_color.stop()


@bot.command(description="Включить мигалки")
async def chase(ctx):
    """
    Комманда "chase", которая включает "мигание" цвета роли,
    запуская change_color() task.
    :param ctx:
    :return:
    """

    # Заканчиваем выполнение функции, eсли у пользователя нет необходимой роли.
    roles = [role.name for role in ctx.author.roles]
    if conf["Police"]["role_name"] not in roles:
        await ctx.respond(embed=et.role_needed, ephemeral=True)
        return

    global chase_status
    chase_status = not chase_status
    text: str = "Мигалки включены!!!"

    if chase_status:
        change_color.start()
    else:
        text = "Мигалки отключены."
        change_color.stop()

    await ctx.respond(text, ephemeral=True)
    return


@tasks.loop(seconds=1)
async def change_color():
    """
    Task, выполняемый раз в 1 секунду.
    Меняет цвет роли - conf["Police"]["role_name"], чередуя синий и красный.
    :return:
    """

    guild = bot.get_guild(SERVER_ID)
    role = discord.utils.get(guild.roles, name=conf["Police"]["role_name"])

    if role.color == discord.Color.red():
        await role.edit(color=discord.Color.blue())
    else:
        await role.edit(color=discord.Color.red())


bot.run(TOKEN)
