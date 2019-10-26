import discord
from discord.ext import commands
import os
import asyncio

class Play(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""
        #await ctx.author.voice.channel.connect()

        print(os.path.exists("res/hello.wav"))
        source = discord.FFmpegPCMAudio("res/hello.wav")
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def record(self, ctx):
        """record 10 seconds to a wav file"""
        
        await ctx.send('Recording 10 seconds of audio')

        sink = discord.WaveSink("res/hello.wav")
        ctx.voice_client.listen(discord.UserFilter(discord.TimedFilter(sink, 10), ctx.author))
        await asyncio.sleep(11)
        await ctx.send('Saving...')
        sink.cleanup()

    @record.before_invoke
    @play.before_invoke
    async def ensure_voice(self, ctx):
        if not discord.opus.is_loaded():
            discord.opus.load_opus('res/libopus.so')
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.command()
    async def stop(self, ctx):
        """Stops and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

class VoiceBurd(commands.Bot):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message_(self, message):
        # don't respond to ourselves
        if message.author == self.user:
            return

        await self.process_commands(message)

        if message.content == 'ping':
            await message.channel.send('pong')



bot = VoiceBurd(command_prefix='!')
bot.add_cog(Play(bot))



with open(".token") as f:
    bot.run(f.read().strip())
