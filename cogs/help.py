import functions
import discord
from discord.ext import menus
from discord.ext import commands
from main import return_guild_count

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
            embed.add_field(name="👤 Accounts", value="`stats`, `creatorstats`, `topsubscribed`, `topcreators`, `bio`, `pfp`, `banner`, `profile`, `junior`, `date`, `nickname`",inline=False)

            embed.add_field(name="🖼️ Images", value="`photos`, `feed`, `latest`, `latestinby`, `latestwith` `latestfeed`, `oldest`, `oldestinby`, `oldestwith`, `oldestfeed`, `frontpage`, `takenin`, `takenof`, `takenofin`, `together`, `cheers`, `comments`, `photostats`, `sortby`, `bookmarked`, `blacklisted`",inline=False)

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
        elif menu == "menus":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "📟 Menu commands",
                description = "These commands utilize the slick menu system! They can also be found in other categories."
            )
            embed.add_field(name="📟 Menus", value="`frontpage`, `photos`, `feed`, `sortby`, `together`, `takenin`, `takenof`, `takenofin`", inline=False)
        elif menu == "legacy":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "👾 Legacy commands",
                description = "These commands are the original versions of some reworked commands."
            )
            embed.add_field(name="👾 Legacy", value="`lfrontpage`, `lsortby`, `ltogether`, `ltakenin`, `ltakenof`, `ltakenofin`", inline=False)
        elif menu == "economyy":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "<:RRtoken:825288414789107762> Economy commands",
                description = "Economy is under development."
            )
            embed.add_field(name="<:RRtoken:825288414789107762> Economy", value="`econprofile (ep)`, `econstats (estats)`, `inventory (inv)`, `play`, `boxes`, `unbox (ub)` `buy`, `gift`, `sell`, `sellall`, `badges`, `daily`, `beg`, `leaderboard`, `boosters`, `use`, `upgrade`, `mirror`, `equip`, `unequip`, `item`", inline=False)
        elif menu == "fun":
            embed = discord.Embed(
                colour= discord.Colour.orange(),
                title = "😹 Fun commands"
            )
            embed.add_field(name="🎮 Minigames", value="`boxsim`", inline=False)
            embed.add_field(name="📑 Checks", value="`cringebiocheck`, `cringenamecheck`, `selfcheers`", inline=False)
            embed.add_field(name="<:wholesome:796100757354053653> Other", value="`adjectiveanimal`", inline=False)
        else:
            embed = discord.Embed(  
                colour= discord.Colour.orange(),
                title = "RecNetBotV2 Command List"
            )

            embed.add_field(name="🛠️ Utility", value="`.help utility`")
            embed.add_field(name="<:RRQuestion:803587583187746847> \"Random\"", value="`.help random`")
            embed.add_field(name="📟 Menus", value="`.help menus`")
            embed.add_field(name="🔎 Search", value="`.help search`")
            embed.add_field(name="😹 Fun", value="`.help fun`")
            embed.add_field(name="📲 API", value="`.help api`")
            embed.add_field(name="👾 Legacy", value="`.help legacy`")
            embed.add_field(name="📖 Other", value="`.help other`")
            #embed.add_field(name="<:RRtoken:825288414789107762> Economy (Early Alpha)", value="`.help economy`")

            rnb_stats = {'TotalCount': None, 'GuildCount': len(self.client.guilds)}

            embed.add_field(name="Other", value=f"[Invite bot](https://discord.com/api/oauth2/authorize?client_id=788632031835324456&permissions=322624&scope=bot) | [Discord](https://discord.gg/GPVdhMa2zK)\n<:discord:803539862435135510> Server count: `{rnb_stats['GuildCount']}`", inline=False)


        functions.embed_footer(ctx, embed)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
