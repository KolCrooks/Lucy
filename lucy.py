from asyncio import run, sleep
from urllib import response
import interactions
from interactions import Embed, ActionRow, Button, ButtonStyle
import dotenv
import os
dotenv.load_dotenv()

bot = interactions.Client(token=os.getenv('TOKEN'))

response = None


async def wait_on_response():
    total = 30
    while not response and total != 0:
        await sleep(1)
        total -= 1
    if not response:
        return "NONE"
    t = response
    response = None
    return t

@bot.component("open")
async def open_response(ctx: interactions.ComponentContext):
    ctx.edit(embeds=[Embed(title="Someone is at the door!")])
    await ctx.send(ctx.author.mention + " opened The Door!")
    response = "OPEN"

@bot.component("deny")
async def deny_response(ctx: interactions.ComponentContext):
    await ctx.send(ctx.author.mention + " denied the person from being let in!")
    response = "DENY"

@bot.component("forward")
async def forward_response(ctx: interactions.ComponentContext):
    await ctx.send(ctx.author.mention + " forwarded the call to there phone!")
    response = "FORWARD"

async def create_handle():
    for c in bot.guilds[0].channels:
        print(c.name)
        if c.name == "buzz-in":
            msg = await c.send(embeds=[Embed(title="Someone is at the door!")],
             components= ActionRow(components=[
                    Button(style=ButtonStyle.SUCCESS, label="Open Door", custom_id="open"),
                    Button(style=ButtonStyle.DANGER, label="Deny", custom_id="deny"),
                    Button(style=ButtonStyle.PRIMARY, label="Forward To Your Phone", custom_id="forward"),
                ]),
            )
@bot.event
async def on_ready():
    await create_handle()
bot.start()