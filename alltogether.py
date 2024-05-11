# DS 2002 Final Project Pt 2
# Grace Saunders and Anagha Chundhury

import openai
import json
from dotenv import load_dotenv
from discord import Intents, Client, Message
from responses import get_response

# open ai api key and discord token: in a comment on canvas assignment because dotenv was not working

# opening csv file with cafe sales targets
csv_file_path = '/Users/gracesaunders/PycharmProjects/ds2002etl/datasets/sales targets.csv'
with open(csv_file_path, 'r') as file:
    csv_text = file.read()

# initialize conversation history
conversation_history = [
    {"role": "system", "content": "You are a helpful assistant knowledgeable on cafe operation. Assist the user in answering"
                                  "questions based on sales targets" + csv_text }
]

# function to ask GPT a question and getting a response, with the ability to specify a character or role
# for the assistant
def ask_openai(question, character="helpful assistant"):
    # append the user's question to the conversation history
    conversation_history.append({"role": "user", "content": question})

    # call the OpenAI API with the conversation history
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history,
        temperature=0.5,  # Adjust for creativity
        max_tokens=150,   # Adjust for response length
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )

    # extract the assistant's answer from the response
    answer = response['choices'][0]['message']['content']

    # append the assistant's answer to the conversation history for context in future interactions
    conversation_history.append({"role": "assistant", "content": answer})

    return answer

# interactive Chat:  This section is definitely functioning properly and works correctly in python, but
# the chat with the bot in discord still shows old answers and doesn't reflect updates in code
while True:
    user_input = input("You: ")
    if user_input.lower() == 'quit':
        break
    print("AI: ", ask_openai(user_input))

from random import choice, randint

# function to set answers based on specific user inputs; does not work in discord (it still shows the default options)
def get_response(user_input: str) -> str:
    lowered: str = user_input.lower()

    if lowered == '':
        return 'Well, you are quiet'
    elif 'hello' in lowered:
        return 'Hello there!'
    elif 'roll dice' in lowered:
        return f'You rolled a {randint(1, 6)}'
    elif 'help' in lowered:
        return f'you can ask questions about the sales goals for the locations of a coffee shop'
    else:
        return choice(['testing1', 'testing2'])


#Step 1: BOT SETUP
intents: Intents = Intents.default()
intents.message_content = True  # NOQA
client: Client = Client(intents=intents)

#Step 2: Message Function
async def send_message(message: Message,user_message: str) -> None:
    if not user_message:
        print('(Message was empty becuase intents were not enabled...prob)')
        return
#check to see if you need to resopnd to private messages
    if is_private := user_message[0] =='?':
        user_message = user_message[1:]

    try:
        response: str= get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#Step 3: Handle the startup of the bot
# this section no longer works - something is going wrong with bot startup that prevents changes from
# reaching discord
@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

#Step 4:  Let's handle the messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user: #The bot wrote the message, or the bot talks to itself
        return
    await send_message(message)

#Step 5 Main Starting point

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()
