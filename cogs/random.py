import functions
import requests
import discord
import random
import json
from discord.ext import commands

class Random(commands.Cog):
    def __init__(self, client):
        self.client = client
    # RANDOM COMMANDS

    # CMD-RANDOMBIO
    @commands.command(aliases=["rb", "rbio"])
    @commands.check(functions.beta_tester)
    async def randombio(self, ctx, amount=1):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        if amount > 5:
            amount = 5
        elif amount < 1:
            amount = 1

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            description = f"<a:spinning:804022054822346823> Searching for {amount} random bio(s)..."
        )
        functions.embed_footer(ctx, embed)
        loading = await ctx.send(embed=embed)

        bio_list = []

        for x in range(amount):
            bio = functions.find_random_bio()
            bio_list.append(bio)

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = "Random bio(s)"
        )

        # make fields for bios
        for x in bio_list:
            account_id = x["account_id"]
            username = functions.id_to_username(account_id)
            display_name = functions.id_to_display_name(account_id)
            bio = x["bio"]
            embed.add_field(name=f"👤 {username} @{display_name}", value=f"```{bio}```[🔗Profile](https://rec.net/user/{username})", inline=False)

        functions.embed_footer(ctx, embed) # get default footer from function
        await loading.delete()
        await ctx.send(author, embed=embed)


    # CMD-CRINGEBIO
    @commands.command(aliases=["cb", "cbio"])
    @commands.check(functions.beta_tester)
    async def cringebio(self, ctx, amount=1):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        if amount > 5:
            amount = 5
        elif amount < 1:
            amount = 1

        bio_list = []

        with open('cringe_bios.json') as data_file:
            cringe_bio_list = json.load(data_file)
            for x in range(amount):
                random_bio = cringe_bio_list[random.randint(0, len(cringe_bio_list)-1)]
                bio_list.append({"account_id": random_bio[0], "bio": random_bio[1]})

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = "Possible cringe bio(s)"
        )

        # make fields for bios
        for bio in bio_list:
            account_id = bio["account_id"]
            username = functions.id_to_username(account_id)
            display_name = functions.id_to_display_name(account_id)
            bio = bio["bio"]
            embed.add_field(name=f"👤 **{display_name}** @{username}", value=f"```{bio}```[🔗Profile](https://rec.net/user/{username})", inline=False)

        embed.add_field(name=f"CHECK IF SOMEONE'S BIO IS CRINGE!", value=f"`.cbc <username>`", inline=False)

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(author, embed=embed)

    # CMD-FASTRANDOMBIO
    @commands.command(aliases=["frb"])
    @commands.check(functions.beta_tester)
    async def fastrandombio(self, ctx, amount=1):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        if amount > 5:
            amount = 5
        elif amount < 1:
            amount = 1

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = "Random bio(s)",
        )

        with open('randombio_list.json') as json_file: 
            data = json.load(json_file)
            for x in range(amount): 
                random_bio = random.randint(0, len(data)-1) 
                username = functions.id_to_username(data[random_bio]["account_id"])
                display_name = functions.id_to_display_name(data[random_bio]["account_id"])
                bio = data[random_bio]["bio"]
                embed.add_field(name=f"👤 **{display_name}** @{username}", value=f"```{bio}```[🔗Profile](https://rec.net/user/{username})", inline=False)

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(author, embed=embed)


    # CMD-RANDOMACCOUNT
    @commands.command(aliases=["raccount"])
    @commands.check(functions.beta_tester)
    async def randomaccount(self, ctx):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        account = functions.find_random_account()
        pfp = functions.id_to_pfp(account['accountId'])

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = f"Random account! @{account['username']}",
        )
        embed.add_field(name="Display name", value=f"`{account['displayName']}`", inline=True)
        embed.add_field(name="Created at", value=f"`{account['createdAt'][:10]}`", inline=True)
        embed.add_field(name="Is junior?", value=f"`{account['isJunior']}`", inline=True)
        embed.add_field(name="Bio", value=f"```{functions.id_to_bio(account['accountId'])}```")
        embed.set_image(url=pfp)
        embed.set_author(name=f"{account['username']}'s profile", url=f"https://rec.net/user/{account['username']}", icon_url=pfp)

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(author, embed=embed)


    # CMD-RANDOMPFP
    @commands.command(aliases=["rpfp"])
    @commands.check(functions.beta_tester)
    async def randompfp(self, ctx):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        pfp = "DefaultProfileImage"
        while pfp == "DefaultProfileImage":
            account = functions.find_random_account()
            pfp = account["profileImage"]

        account_id = account["accountId"]
        username = account["username"]

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = f"Random profile picture!",
            description = f"[🔗 RecNet post](https://rec.net/image/{pfp}) *(might not exist)*"
        )
        embed.set_image(url=f"https://img.rec.net/{pfp}")
        embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(account_id))

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(author, embed=embed)


    # CMD-RANDOMLOADSCREEN
    @commands.command(aliases=["rls"])
    @commands.check(functions.beta_tester)
    async def randomloadscreen(self, ctx):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        loading_screens = requests.get("https://cdn.rec.net/config/LoadingScreenTipData").json()
        load_screen = loading_screens[random.randint(0, len(loading_screens)-1)]
   
        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = load_screen["Title"],
            description = f"{load_screen['Message']}\n\n*Made in*\n📆 `{load_screen['CreatedAt'][:10]}`\n⏰ `{load_screen['CreatedAt'][11:16]} UTX`"
        )
        embed.set_image(url=f"https://img.rec.net/{load_screen['ImageName']}?width=720")

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)

    
    # CMD-RANDOMIMG
    @commands.command(aliases=["rimg"])
    @commands.check(functions.beta_tester)
    async def randomimg(self, ctx, amount=1):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        if amount > 5:
            amount = 5
        elif amount < 1:
            amount = 1

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            description = f"<a:spinning:804022054822346823> Searching for {amount} random image(s)..."
        )
        functions.embed_footer(ctx, embed)
        loading = await ctx.send(embed=embed)

        img_string = ""
        for x in range(amount):
            random_img = functions.find_random_img()

            tagged = functions.get_tagged_accounts_string(random_img, True)

            if amount == 1:
                username = functions.id_to_username(random_img['PlayerId'])
                room_name = functions.id_to_room_name(random_img['RoomId'])
                if room_name:
                    room_string = f"\n🚪 [`^{room_name}`](https://rec.net/room/{room_name})\n"
                else:
                    room_string = "\n"
                    
                embed=discord.Embed(
                    colour=discord.Colour.orange(),
                    title=f"Random image of @{username}, taken by @{functions.id_to_username(random_img['PlayerId'])}",
                    description=f"🔗 **[RecNet post](https://rec.net/image/{random_img['Id']})**{room_string}<:CheerGeneral:803244099510861885> `{random_img['CheerCount']}` 💬 `{random_img['CommentCount']}`\n📆 `{random_img['CreatedAt'][:10]}` ⏰ `{random_img['CreatedAt'][11:16]} UTX`\n{tagged}"
                )
                embed.set_image(url=f"https://img.rec.net/{random_img['ImageName']}")
                embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(random_img['PlayerId']))
            else:
                img_string += f"https://rec.net/image/{random_img['Id']}\n**{functions.id_to_display_name(random_img['PlayerId'])}** @{functions.id_to_username(random_img['PlayerId'])}\n<:CheerGeneral:803244099510861885> `{random_img['CheerCount']}` 💬 `{random_img['CommentCount']}`\n{tagged}\n\n"

        await loading.delete()
        if amount == 1:
            await ctx.send(f"{author}\n",embed=embed)   
        else:
            await ctx.send(f"{author}\n{img_string}")

    # CMD-RANDOMROOM
    @commands.command(aliases=["rroom"])
    @commands.check(functions.beta_tester)
    async def randomroom(self, ctx):
        functions.log(ctx.guild.name, ctx.author, ctx.command)
        
        author = f"<@{ctx.author.id}>"

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            description = f"<a:spinning:804022054822346823> Searching for a random room..."
        )
        functions.embed_footer(ctx, embed)
        loading = await ctx.send(embed=embed)

        room = functions.find_random_room()
        room_embed = functions.room_embed(room, True)

        functions.embed_footer(ctx, room_embed) # get default footer from function

        await loading.delete()
        await ctx.send(author, embed=room_embed)


    # CMD-RANDOMEVENT
    @commands.command(aliases=["revent"])
    @commands.check(functions.beta_tester)
    async def randomevent(self, ctx):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        event = functions.find_random_event()
        event_creator = functions.id_to_username(event['CreatorPlayerId'])
        event_description = event['Description']
        try:
            event_room = f"[^{functions.get_room_json(event['RoomId'], True)['Name']}](https://rec.net/room/{functions.get_room_json(event['RoomId'], True)['Name']})"
        except:
            event_room = "`Dorm room`"
        if not event["Description"]:
            event_description = "None"

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = f"{event['Name'] }",
            description = f"**Description**```{event_description}```\n**Information**\n🚪 Room: {event_room}\n👥 Attendees: `{event['AttendeeCount']}`\n📆 Start time: `{event['StartTime'][:10]}`, at ⏰ `{event['StartTime'][11:16]} UTX`\n🚷 End time: `{event['EndTime'][:10]}`, at ⏰ `{event['EndTime'][11:16]} UTX`",
            url=f"https://rec.net/event/{event['PlayerEventId']}"
        )

        embed.set_author(name=f"{event_creator}'s profile", url=f"https://rec.net/user/{event_creator}", icon_url=functions.id_to_pfp(event['CreatorPlayerId']))
        embed.set_image(url=f"https://img.rec.net/{event['ImageName']}?width=720")
        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)


    # CMD-RANDOMIMGOF
    @commands.command(aliases=["rimgof", "rio"])
    @commands.check(functions.beta_tester)
    async def randomimgof(self, ctx, profile):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        account = functions.check_account_existence_and_return(profile)
        if account:
            feed = functions.id_to_feed(account['account_id'])
            
            if feed:
                random_feed = feed[random.randint(0, len(feed)-1)]
                username = functions.id_to_username(account['account_id'])
                tagged = functions.get_tagged_accounts_string(random_feed)
                
                room_name = functions.id_to_room_name(random_feed['RoomId'])
                if room_name:
                    room_string = f"\n🚪 [`^{room_name}`](https://rec.net/room/{room_name})\n"
                else:
                    room_string = "\n"
                    
                embed=discord.Embed(
                    colour=discord.Colour.orange(),
                    title=f"Random image of @{username}, taken by @{functions.id_to_username(random_feed['PlayerId'])}",
                    description=f"🔗 **[RecNet post](https://rec.net/image/{random_feed['Id']})**{room_string}<:CheerGeneral:803244099510861885> `{random_feed['CheerCount']}` 💬 `{random_feed['CommentCount']}`\n📆 `{random_feed['CreatedAt'][:10]}` ⏰ `{random_feed['CreatedAt'][11:16]} UTX`\n{tagged}"
                )
                embed.set_image(url=f"https://img.rec.net/{random_feed['ImageName']}")
                embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(account['account_id']))
            else:
                embed = functions.error_msg(ctx, f"User `@{profile}` doesn't appear in any post!")
        else:
            embed = functions.error_msg(ctx, f"User `@{profile}` doesn't exist!")

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)

    @randomimgof.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = functions.error_msg(ctx, "Please include in an username!")
            
            await ctx.send(embed=embed)
        else:
            pass


    # CMD-RANDOMIMGBY
    @commands.command(aliases=["rimgby", "rib"])
    @commands.check(functions.beta_tester)
    async def randomimgby(self, ctx, profile):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        account = functions.check_account_existence_and_return(profile)
        if account:
            photos = functions.id_to_photos(account['account_id'])
            
            if photos:
                random_photos = photos[random.randint(0, len(photos)-1)]
                username = functions.id_to_username(account['account_id'])
                tagged = functions.get_tagged_accounts_string(random_photos)
                
                room_name = functions.id_to_room_name(random_photos['RoomId'])
                if room_name:
                    room_string = f"\n🚪 [`^{room_name}`](https://rec.net/room/{room_name})\n"
                else:
                    room_string = "\n"

                embed=discord.Embed(
                    colour=discord.Colour.orange(),
                    title=f"Random image taken by @{username}",
                    description=f"🔗 **[RecNet post](https://rec.net/image/{random_photos['Id']})**{room_string}<:CheerGeneral:803244099510861885> `{random_photos['CheerCount']}` 💬 `{random_photos['CommentCount']}`\n📆 `{random_photos['CreatedAt'][:10]}` ⏰ `{random_photos['CreatedAt'][11:16]} UTX`\n{tagged}"
                )
                embed.set_image(url=f"https://img.rec.net/{random_photos['ImageName']}")
                embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(account['account_id']))
            else:
                embed = functions.error_msg(ctx, f"User `@{account['username']}` hasn't shared a single post!")
        else:
            embed = functions.error_msg(ctx, f"User `@{profile}` doesn't exist!")

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)

    @randomimgby.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = functions.error_msg(ctx, "Please include in an username!")
            
            await ctx.send(embed=embed)
        else:
            pass

    
    # CMD-RANDOMIMGBYIN
    @commands.command(aliases=["rimgbyin", "ribi"])
    @commands.check(functions.beta_tester)
    async def randomimgbyin(self, ctx, profile, room_name):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        account = functions.check_account_existence_and_return(profile)
        if account:
            room = functions.get_room_json(room_name)
            if room:
                photos = functions.id_to_photos(account['account_id'])
                
                if photos:
                    found_photos = []
                    # find photos in room
                    for photo in photos:
                        if photo['RoomId'] == room['RoomId']:
                            found_photos.append(photo)

                    if found_photos:
                        random_photos = found_photos[random.randint(0, len(found_photos)-1)]
                        username = functions.id_to_username(account['account_id'])
                        tagged = functions.get_tagged_accounts_string(random_photos)
                        
                        room_name = functions.id_to_room_name(random_photos['RoomId'])
                        embed=discord.Embed(
                            colour=discord.Colour.orange(),
                            title=f"Random image taken by @{username} in ^{room_name}",
                            description=f"🔗 **[RecNet post](https://rec.net/image/{random_photos['Id']})**\n🚪 [`^{room_name}`](https://rec.net/room/{room_name})\n<:CheerGeneral:803244099510861885> `{random_photos['CheerCount']}` 💬 `{random_photos['CommentCount']}`\n📆 `{random_photos['CreatedAt'][:10]}` ⏰ `{random_photos['CreatedAt'][11:16]} UTX`\n{tagged}"
                        )
                        embed.set_image(url=f"https://img.rec.net/{random_photos['ImageName']}")
                        embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(account['account_id']))
                    else:
                        embed = functions.error_msg(ctx, f"User `@{account['username']}` hasn't shared a single post in `^{room['Name']}`!")
                else:
                    embed = functions.error_msg(ctx, f"User `@{account['username']}` hasn't shared a single post!")
            else:
                embed = functions.error_msg(ctx, f"Room `^{room_name}` doesn't exist!")
        else:
            embed = functions.error_msg(ctx, f"User `@{profile}` doesn't exist!")

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)

    @randomimgbyin.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = functions.error_msg(ctx, "Please include in an username and room!\nUsage: `.randomimgbyin <user> <room>`")
            
            await ctx.send(embed=embed)
        else:
            pass


    # CMD-RANDOMIMGOFIN
    @commands.command(aliases=["rimgofin", "rioi"])
    @commands.check(functions.beta_tester)
    async def randomimgofin(self, ctx, profile, room_name):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        account = functions.check_account_existence_and_return(profile)
        if account:
            room = functions.get_room_json(room_name)
            if room:
                photos = functions.id_to_feed(account['account_id'])
                
                if photos:
                    found_photos = []
                    # find photos in room
                    for photo in photos:
                        if photo['RoomId'] == room['RoomId']:
                            found_photos.append(photo)

                    if found_photos:
                        random_photos = found_photos[random.randint(0, len(found_photos)-1)]
                        username = functions.id_to_username(account['account_id'])
                        tagged = functions.get_tagged_accounts_string(random_photos)
                        
                        room_name = functions.id_to_room_name(random_photos['RoomId'])
                        embed=discord.Embed(
                            colour=discord.Colour.orange(),
                            title=f"Random image taken of @{username} in ^{room_name}",
                            description=f"🔗 **[RecNet post](https://rec.net/image/{random_photos['Id']})**\n🚪 [`^{room_name}`](https://rec.net/room/{room_name})\n<:CheerGeneral:803244099510861885> `{random_photos['CheerCount']}` 💬 `{random_photos['CommentCount']}`\n📆 `{random_photos['CreatedAt'][:10]}` ⏰ `{random_photos['CreatedAt'][11:16]} UTX`\n{tagged}"
                        )
                        embed.set_image(url=f"https://img.rec.net/{random_photos['ImageName']}")
                        embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(account['account_id']))
                    else:
                        embed = functions.error_msg(ctx, f"User `@{account['username']}` doesn't appear in `^{room['Name']}`!")
                else:
                    embed = functions.error_msg(ctx, f"User `@{profile}` doesn't appear in `^{room_name}` at all!")
            else:
                embed = functions.error_msg(ctx, f"Room `^{room_name}` doesn't exist!")
        else:
            embed = functions.error_msg(ctx, f"User `@{profile}` doesn't exist!")

        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(embed=embed)


    @randomimgofin.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = functions.error_msg(ctx, "Please include in an username and room!\nUsage: `.randomimgofin <user> <room>`")
            
            await ctx.send(embed=embed)
        else:
            pass



    # CMD-RANDOMIMGIN
    @commands.command(aliases=["rimgin", "rii"])
    @commands.check(functions.beta_tester)
    async def randomimgin(self, ctx, room_name):
        functions.log(ctx.guild.name, ctx.author, ctx.command)

        room = functions.get_room_json(room_name)
        if room:
            author = f"<@{ctx.author.id}>"

            embed=discord.Embed(
                colour=discord.Colour.orange(),
                description = f"<a:spinning:804022054822346823> Loading >10,000 pictures taken in `^{room['Name']}`, and picking one randomly..."
            )
            functions.embed_footer(ctx, embed)
            loading = await ctx.send(embed=embed)

            room_photos = functions.get_photos_in_room(room_name)
            if room_photos:
                random_photo = room_photos[random.randint(0, len(room_photos)-1)]
                tagged = functions.get_tagged_accounts_string(random_photo)
                room_photo_count = len(room_photos)
                if room_photo_count > 9999:
                    room_photo_count = ">10000"

                embed=discord.Embed(
                    colour=discord.Colour.orange(),
                    title=f"Random image taken in ^{room['Name']}",
                    description=f"🔗 **[RecNet post](https://rec.net/image/{random_photo['Id']})**\n🚪 [`^{room['Name']}`](https://rec.net/room/{room['Name']})\n<:CheerGeneral:803244099510861885> `{random_photo['CheerCount']}` 💬 `{random_photo['CommentCount']}`\n📆 `{random_photo['CreatedAt'][:10]}` ⏰ `{random_photo['CreatedAt'][11:16]} UTX`\n{tagged}\n🖼️ Pictures shared in `^{room['Name']}`: `{room_photo_count}`"
                )
                embed.set_image(url=f"https://img.rec.net/{random_photo['ImageName']}")
                username = functions.id_to_username(random_photo['PlayerId'])
                embed.set_author(name=f"{username}'s profile", url=f"https://rec.net/user/{username}", icon_url=functions.id_to_pfp(random_photo['PlayerId']))
            else:
                embed = functions.error_msg(ctx, f"Not a single picture has been taken in `^{room['Name']}`")
        else:
            embed = functions.error_msg(ctx, f"Room `^{room_name}` doesn't exist!")

        await loading.delete()
        functions.embed_footer(ctx, embed) # get default footer from function
        await ctx.send(author, embed=embed)

    @randomimgin.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = functions.error_msg(ctx, "Please include in a room!")
            
            await ctx.send(embed=embed)
        else:
            pass

        
def setup(client):
    client.add_cog(Random(client))