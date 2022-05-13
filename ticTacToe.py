import discord
from discord.ext import commands
import random

client = commands.Bot(command_prefix="!")

plyr1 = ""
plyr2 = ""
turn = ""
gameOver = True
board = []


# possible ways to win the game
game_win_cases = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [8, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [8, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tic_tac_toe(ctx, p1: discord.Member, p2: discord.Member):
    global turn
    global count
    global plyr1
    global plyr2
    global play_turn
    global gameOver

    # condition if game is over then refresh board
    if gameOver:
        global board
        # create an empty board
        board = [":white_large_square:",":white_large_square:", ":white_large_square:"
                 , ":white_large_square:", ":white_large_square:", ":white_large_square:"
                 , ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        plyr1 = p1
        plyr2 = p2

        # print game board
        line = ""
        for x in range(len(board)):
            # add a new line when end at each line
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # Randomize a choice on who gets to go first
        num = random.randint(1, 2)
        if num == 1:
            turn = plyr1
            await ctx.send("It is <@" + str(plyr1.id) + ">'s turn")
        else:
            turn = plyr2
            await ctx.send("It is <@" + str(plyr2.id) + ">'s turn")

@client.command()
async def place(ctx, pos: int):
    global turn
    global plyr1
    global plyr2
    global board
    global count
    global gameOver

    # check user place and game situation if someone has won or if its a tie
    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == plyr1:
                mark = ":regional_indicator_x:"
            elif turn == plyr2:
                mark = ":o2:"
            # Check if position is valid on the board
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print board after completing a turn
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                # check for winner if there is one
                checkWinner(game_win_cases, mark)
                print(count)
                if gameOver:
                    await ctx.send(mark + "wins!!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!!")


def checkWinner(game_win_cases, mark):
    global gameOver
    for condition in game_win_cases:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tic_tac_toe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players.")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


client.run()
