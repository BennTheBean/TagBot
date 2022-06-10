import discord
import gspread
import os

sa = gspread.service_account(filename="tag-scores-c365003a50fb.json")
sh = sa.open("tagscores")

wks = sh.worksheet("Data")
wks2 = sh.worksheet("Leader")

tagdata = {
  "Empty":0
}
order = sorted(tagdata, key=tagdata.get, reverse=False)

def update():
  global order
  tagdata.clear()
  for i in range(15):
          tagdata[wks.acell('A' + str(i+20)).value + ": " + str(wks.acell('C' + str(i+20)).value)] = wks.acell('C' + str(i+20)).value
  order.clear()
  order = sorted(tagdata, key=tagdata.get, reverse=False)

def annoyingstuff(tagger, tagged):
  cell = wks.find(tagger+".")
  cell2 = wks.find(tagged)
  current = wks.acell(chr(cell2.col+64)+str(cell.row)).value
  wks.update_acell(chr(cell2.col+64)+str(cell.row), str(int(current) + 1))

client = discord.Client()

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('!leader'):
        update()
        for i in range(len(tagdata)):
            await message.channel.send(str(i+1) + ". " + order[i])
  elif message.content.startswith('!update'):
        update()
        for i in range(len(tagdata)):
          wks2.update_acell('B' + str(i+2), order[i])
        await message.channel.send("Updated")
  elif message.content.startswith('!tag'):
      tagger = message.content.split(" ",2)[1]
      tagged = message.content.split(" ",2)[2]
      await message.channel.send("<@&984069096872222770> " + tagger + " Tagged " + tagged)
      annoyingstuff(tagger.lower(), tagged.lower())
client.run(os.environ['DISCORD_TOKEN'])
