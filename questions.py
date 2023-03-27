import discord
import random
import Levenshtein
import json
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

# load questions from questions.json file
with open('questions.json', 'r', encoding='utf-8') as f:
    questions = json.load(f)

# load user data from user_data.json file
try:
    with open('user_data.json', 'r') as f:
        user_data = json.load(f)
except json.decoder.JSONDecodeError:
    user_data = {}

# function to get a random question for a user
def get_question(user):
    # create new entry in user_data if user is not already in it
    if user not in user_data:
        user_data[user] = {'score': 0, 'answered_questions': [], 'current_question': None}
    # get list of questions user has not yet answered
    unanswered_questions = [q for q in questions if q['id'] not in user_data[user]['answered_questions']]
    if not unanswered_questions:
        # user has answered all questions
        return "Well done! You have answered all the available questions!"
    # choose a random question from the list of unanswered questions
    question = random.choice(unanswered_questions)
    # update user's current question in their user data
    user_data[user]['current_question'] = question['id']
    return question['question']


# command to ask a user their current question
@bot.command()
async def current(ctx):
    user = str(ctx.author.id)
    current_question_id = user_data[user]['current_question']
    current_question = next(q for q in questions if q['id'] == current_question_id)['question']
    await ctx.send(f"Your current question is: {current_question}")

# command to get a new question
@bot.command()
async def ask(ctx):
    user = str(ctx.author.id)
    question = get_question(user)
    if question == "Well done! You have answered all the available questions!":
        await ctx.send(f"{ctx.author.mention}, you have answered all the available questions!")
    else:
        await ctx.send(f"{ctx.author.mention}, here is your question: {question}")


@bot.command()
async def answer(ctx, *, user_answer):
    user = str(ctx.author.id)
    current_question_id = user_data[user]['current_question']
    correct_answer = next(q for q in questions if q['id'] == current_question_id)['answer']
    # check if the user's answer is correct using Levenshtein distance
    if Levenshtein.distance(user_answer.lower(), correct_answer.lower()) <= 2:
        # answer is correct, give the user a point and update their user data
        user_data[user]['score'] += 3
        user_data[user]['answered_questions'].append(current_question_id)
        await ctx.message.add_reaction("✅")  # add a check mark emoji as a reaction to the user's message
        await ctx.send(f"{ctx.author.mention}, that is correct! You now have {user_data[user]['score']} points.")
    else:
        # answer is incorrect
        user_data[user]['score'] -= 1
        await ctx.message.add_reaction("❌")  # add an X mark emoji as a reaction to the user's message
        await ctx.send(f"{ctx.author.mention}, sorry, \"{user_answer}\" is incorrect. Please try again. Minus 1 point for you.")
    
    # save updated user data
    save_user_data()




# command to check a user's current score
@bot.command()
async def points(ctx):
    user = str(ctx.author.id)
    score = user_data[user]['score']
    await ctx.send(f"{ctx.author.mention}, you currently have {score} points.")

# save user data to user_data.json file every time it is updated
def save_user_data():
    with open('user_data.json', 'w') as f:
        json.dump(user_data, f)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Sorry, that command does not exist.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please provide a valid answer.")
    else:
        await ctx.send("An error occurred. Please try again later.")

# command to display leaderboard
@bot.command()
async def leaderboard(ctx):
    sorted_users = sorted(user_data.items(), key=lambda x: x[1]['score'], reverse=True)
    leaderboard_str = "```"
    leaderboard_str += "LEADERBOARD\n"
    for i, user in enumerate(sorted_users):
        user_id = user[0]
        score = user[1]['score']
        user_name = await bot.fetch_user(int(user_id))
        leaderboard_str += f"{i+1}. {user_name.name}: {score}\n"
    leaderboard_str += "```"
    await ctx.send(leaderboard_str)

# command to reset a user's score and answered questions
@bot.command()
async def reset(ctx):
    user = str(ctx.author.id)
    user_data[user]['score'] = 0
    user_data[user]['answered_questions'] = []
    await ctx.send(f"{ctx.author.mention}, your score and answered questions have been reset.")

    # save updated user data
    save_user_data()

# event to print message in console when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')


# run the bot
bot.run('MTA4MjA3ODE3MzgxNjE4MDg1OA.GWjEwv.gmm4xm4Gf3YNuslYLOOWGyBOZ79wdY8rFavSJI')
