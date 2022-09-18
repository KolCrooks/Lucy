import asyncio
from asyncio import sleep
import interactions
import threading
from interactions import Embed, ActionRow, Button, ButtonStyle

from quart import Quart
from twilio.twiml.voice_response import VoiceResponse

# import dotenv
import os

# dotenv.load_dotenv()

bot = interactions.Client(token=os.getenv('TOKEN'))

response = None
msg = None
full = ActionRow(components=[
    Button(style=ButtonStyle.SUCCESS, label="Open Door", custom_id="open"),
    Button(style=ButtonStyle.DANGER, label="Deny", custom_id="deny"),
    Button(style=ButtonStyle.PRIMARY, label="Forward To Your Phone", custom_id="forward"),
])
full_grey = ActionRow(components=[
    Button(style=ButtonStyle.SUCCESS, disabled=True, label="Open Door", custom_id="open"),
    Button(style=ButtonStyle.DANGER, disabled=True, label="Deny", custom_id="deny"),
    Button(style=ButtonStyle.PRIMARY, disabled=True, label="Forward To Your Phone", custom_id="forward"),
])


async def wait_on_response():
    global response
    total = 30
    while not response and total != 0:
        await sleep(1)
        total -= 1
    if not response:
        return "NONE", None
    t = response
    response = None
    return t


@bot.component("open")
async def open_response(ctx: interactions.ComponentContext):
    global response
    await msg.edit(embeds=[Embed(title="Their is someone at the door!")], components=full_grey)
    await ctx.send(ctx.author.mention + " opened The Door!")
    response = ("OPEN", int(ctx.author.id))


@bot.component("deny")
async def deny_response(ctx: interactions.ComponentContext):
    global response
    await msg.edit(embeds=[Embed(title="Their is someone at the door!")], components=full_grey)
    await ctx.send(ctx.author.mention + " denied the person from being let in!")
    response = ("DENY", int(ctx.author.id))


@bot.component("forward")
async def forward_response(ctx: interactions.ComponentContext):
    global response
    await msg.edit(embeds=[Embed(title="Their is someone at the door!")], components=full_grey)
    await ctx.send(ctx.author.mention + " forwarded the call to there phone!")
    response = ("FORWARD", int(ctx.author.id))


async def create_handle():
    global msg
    for c in bot.guilds[0].channels:
        print(c.name)
        if c.name == "buzz-in":
            msg = await c.send(embeds=[Embed(title="Their is someone at the door!")],
             components=full,
            )
@bot.event
async def on_ready():
    print("READY")


app = Quart(__name__)

users = {
    250726400149946368: '203-313-0500',
    405116535322050560: '604-367-3623',
    195752001982824448: '778-683-6857'
}

@app.route("/voice", methods=['GET', 'POST'])
async def voice():
    """Respond to incoming phone calls with a 'Hello world' message"""
    print("yo")
    await create_handle()
    result, id = await wait_on_response()

    # Start our TwiML response
    resp = VoiceResponse()

    if result == "OPEN":
        resp.play(digits=9, loop=10)
    elif result == "FORWARD":
        resp.dial(users[id])

    return str(resp)


if __name__ == "__main__":
    bot._loop.create_task(app.run_task(port=8080))
    bot.start()
