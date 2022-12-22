import openai
import discord
from keep_alive import keep_alive
import os

api_token = os.environ['api_token']
bot_api = os.environ['token_bot']
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
openai.api_key = api_token

keep_alive()


@client.event
async def on_message(message):
  global bot_state  # Declara que a variável bot_state é global e pode ser modificada nesta função
  try:
    if message.author == client.user:
      return

    if message.content.startswith('*'):
      if bot_state == "pending":
        await message.channel.send(
          "Aguarde, o bot está ocupado com uma outra pergunta.")
        return  # Interrompe a execução da função

      bot_state = "pending"  # Altera o estado do bot para "pending"
      response = openai.Completion.create(engine="text-davinci-003",
                                          prompt=message.content[1:],
                                          max_tokens=2000,
                                          temperature=0.5,
                                          top_p=1,
                                          frequency_penalty=0,
                                          presence_penalty=0,
                                          n=1)
      response_text = response["choices"][0].text
      if len(response_text) >= 1980:
        substrings = [
          response_text[i:i + 1980] for i in range(0, len(response_text), 1980)
        ]
        for substring in substrings:
          await message.channel.send("```js\n" + substring + "```")
      else:
        await message.channel.send("```js\n" + response_text + "```")

    bot_state = "idle"  # Altera o estado do bot para "idle" novamente
  except Exception as e:
    bot_state = "idle"  # Altera o estado do bot para "idle" novamente
    await message.channel.send("Ocorreu um erro: " + str(e))


client.run(bot_api)
