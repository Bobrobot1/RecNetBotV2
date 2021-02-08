import functions
import discord
from discord.ext import commands


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.check(functions.beta_tester)
    async def help(self, ctx, menu=None):
        if menu == "utility":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "🛠️ Utility commands",
            )
            embed.add_field(name="👤 Accounts", value="`stats`, `bio`, `pfp`, `banner`, `profile`, `junior`, `date`, `nickname`",inline=False)

            embed.add_field(name="🖼️ Images", value="`latest`, `latestin`, `latestwith` `latestfeed`, `oldest`, `oldestin`, `oldestwith`, `oldestfeed`, `frontpage`, `takenin`, `takenof`, `together`, `cheers`, `comments`, `pictures`, `sortby`, `bookmarked`",inline=False)

            embed.add_field(name="🚪 Rooms", value="`roominfo`, `roomsby`, `featured`, `placement`",inline=False)

            embed.add_field(name="<:RRQuestion:803587583187746847> Other", value="`apistatus`, `latestevents`, `shortcuts`", inline=False)
        elif menu == "other":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "📖 Other commands",
                description = "`doc`, `invite`"
            )   
        elif menu == "random":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "<:RRQuestion:803587583187746847> \"Random\" commands",  
            )

            embed.add_field(name="🖼️ Images", value="`randomimg`, `randomimgof`, `randomimgofin`,`randomimgby`, `randomimgbyin`, `randomimgin`, `randompfp`",inline=False)

            embed.add_field(name="📜 Bios", value="`randombio`, `cringebio`, `fastrandombio`",inline=False)

            embed.add_field(name="<:RRQuestion:803587583187746847> Other", value="`randomaccount`, `randomroom`, `randomevent`, `randomloadscreen`",inline=False)

        elif menu == "search":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "🔎 Search commands",
            )
            embed.add_field(name="📆 Events", value="`eventsearch`",inline=False)
        elif menu == "api":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "📲 API commands",
            )
            embed.add_field(name="👤 Accounts", value="`accountdata`, `accountid`",inline=False)

            embed.add_field(name="🖼️ Images", value="`imageid`",inline=False)

            embed.add_field(name="These commands are experimental!", value="They will probably all be combined into one command eventually. As of now, they're used to do simple API calls.")
        else:
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "RecNetBotV2 Command List"
            )

            embed.add_field(name="🛠️ Utility", value="`.help utility`")
            embed.add_field(name="<:RRQuestion:803587583187746847> \"Random\"", value="`.help random`")
            embed.add_field(name="🔎 Search", value="`.help search`")
            embed.add_field(name="📲 API", value="`.help api`")
            embed.add_field(name="📖 Other", value="`.help other`")
        
       
        functions.embed_footer(ctx, embed)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))