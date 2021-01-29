import requests
import discord
import arrow
import random
import asyncio

img_quality = 720
image_dict = {"Id": None, "ImageName": None, "CheerCount": 0, "CommentCount": 0}

# Global functions
def log(server, user, command):
    print(f'\n{server} > {user} > {command}')

def get_date():
    return arrow.now() # current date

def is_it_me(ctx):
    return ctx.author.id == 293008770957836299 # Jegarde's Discord Id

def beta_tester(ctx):
    user_roles = ctx.author.roles
    role = discord.utils.find(lambda r: r.name == 'V2 Tester', ctx.guild.roles)
    is_beta_tester = role in user_roles
    return is_beta_tester

def check_account_existence_and_return(username):
    check = requests.get(f"https://accounts.rec.net/account?username={username}").ok
    print(check)
    return_dict = {}
    if check:
        account_id = username_to_id(username)
        username = id_to_username(account_id)
        return_dict["account_id"] = account_id
        return_dict["username"] = username
        print(return_dict)
        return return_dict
    else: # account doesn't exist
        print(f"Account not found! ({username})")
        return False

def map_image_data(arg, dict):
    if image_dict[dict] < arg[dict]:
        image_dict["Id"] = arg["Id"] 
        image_dict["ImageName"] = arg["ImageName"] 
        image_dict["CheerCount"] = arg["CheerCount"] 
        image_dict["CommentCount"] = arg["CommentCount"] 
    return arg[dict]

def map_func(arg, dict):
    return arg[dict]

def get_room_json(room, is_id=False):
    try:
        if not is_id:
            room_data = requests.get(f"https://api.rec.net/roomserver/rooms/search?query={room}", timeout=10).json()
            if room_data["TotalResults"] == 0:
                # Room doesn't exist!
                return None

            for x in room_data["Results"]:
                if x["Name"].casefold() == room.casefold():
                    room_id = x["RoomId"]
                    break
        else:
            if requests.get(f"https://api.rec.net/roomserver/rooms/{room}", timeout=10).ok:
                room_id = room
            else:
                return None

        print(room_id)
        room_json = requests.get(f"https://api.rec.net/roomserver/rooms/{room_id}/?include=366").json()

        return room_json
    except:
        return None
        
def get_room_placement(room):
    hot_rooms = requests.get("https://api.rec.net/roomserver/rooms/hot?take=1000").json()["Results"]
    print("get_room_placement")

    placement = 0
    for x in hot_rooms:
        if x["Name"].casefold() == room.casefold():
            return placement
        placement += 1
    return "<1000"

def id_to_username(account_id):
    # Get and return account data based on id
    return requests.get(f"https://accounts.rec.net/account/{account_id}").json()["username"]

def id_to_account_data(account_id):
    # Get and return account data based on id
    # If account doesn't exist, return None
    return requests.get(f"https://accounts.rec.net/account/{account_id}").json()

def id_to_pfp(account_id, cropped=True, return_link=True):
    account_pfp = id_to_account_data(account_id)["profileImage"]
    if cropped:
        return f"https://img.rec.net/{account_pfp}?cropSquare=true"
    else:
        if return_link:
            return f"https://img.rec.net/{account_pfp}"
        else: 
            return account_pfp

def id_to_bio(account_id):
    return requests.get(f"https://accounts.rec.net/account/{account_id}/bio").json()["bio"]

def id_to_banner(account_id, return_link=True):
    try:
        account_banner = id_to_account_data(account_id)["bannerImage"]
        if return_link:
            return f"https://img.rec.net/{account_banner}"
        else: 
            return account_banner
    except:
        return None

def id_to_display_name(account_id):
    return id_to_account_data(account_id)["displayName"]

def id_to_all_cheers(account_id):
    photos = id_to_photos(account_id)
    map_result = list(map(lambda x: map_func(x, "CheerCount"), photos))
    return map_result

def id_to_all_comments(account_id):
    photos = id_to_photos(account_id)
    map_result = list(map(lambda x: map_func(x, "CommentCount"), photos))
    return map_result

def id_to_creation_date(account_id):
    return id_to_account_data(account_id)["createdAt"]  

def id_to_is_junior(account_id):
    return id_to_account_data(account_id)["isJunior"]  

def id_to_latest_photo(account_id):
    photos = requests.get(f"https://api.rec.net/api/images/v4/player/{account_id}?take=1").json()
    if photos:
        return photos[0]
    else:
        return None

def id_to_latest_feed(account_id):
    feed = requests.get(f"https://api.rec.net/api/images/v3/feed/player/{account_id}?take=1").json()
    if feed:
        return feed[0]
    else:
        return None

def id_to_oldest_photo(account_id):
    photos = id_to_photos(account_id)
    if photos:
        return photos[len(photos)-1]
    else:
        return None

def id_to_oldest_feed(account_id):
    feed = id_to_feed(account_id)
    if feed:
        return feed[len(feed)-1]
    else:
        return None

def id_to_photos(account_id):
    return requests.get(f"https://api.rec.net/api/images/v4/player/{account_id}?take=100000").json()

def id_to_feed(account_id):
    return requests.get(f"https://api.rec.net/api/images/v3/feed/player/{account_id}?take=100000").json()

def id_to_cheer_stats(account_id):
    global image_dict
    photos = id_to_photos(account_id)

    image_dict = {"Id": None, "ImageName": None, "CheerCount": 0, "CommentCount": 0}
    map_result = map(lambda x: map_image_data(x, "CheerCount"), photos)

    total_cheers = sum(list(map_result))

    return_dict = {"most_cheered": image_dict, "total_cheers": total_cheers}
    return return_dict

def id_to_comment_stats(account_id):
    global image_dict
    photos = id_to_photos(account_id)

    image_dict = {"Id": None, "ImageName": None, "CheerCount": 0, "CommentCount": 0}
    map_result = map(lambda x: map_image_data(x, "CommentCount"), photos)

    total_comments = sum(list(map_result))

    return_dict = {"most_commented": image_dict, "total_comments": total_comments}
    return return_dict

def username_to_id(account_name):
    # Get and return account's id based on name
    return requests.get(f"https://accounts.rec.net/account?username={account_name}").json()["accountId"]

def room_embed(room_name, is_json=False):
    if is_json:
        room = room_name
    else:
        room = get_room_json(room_name)
        
    if room:
        r_name = room["Name"]
        
        # Roles
        owner_username = id_to_username(room["CreatorAccountId"])
        owner_pfp = id_to_pfp(room["CreatorAccountId"])
        role_count = len(room["Roles"])
        
        # Placement
        placement = get_room_placement(r_name)

        # Stats
        cheers = room["Stats"]["CheerCount"]
        favorites = room["Stats"]["FavoriteCount"]
        visitor_count = room["Stats"]["VisitorCount"]
        visit_count = room["Stats"]["VisitCount"]

        #visitor_cheer_ratio = round((cheers / visitor_count) * 100)
        #visit_visitor_ratio = round((visitor_count / visit_count) * 100)
        
        # Subrooms
        subrooms = ""
        for i in room["SubRooms"]:
            subroom_name = i["Name"]
            subrooms += f"{subroom_name}, "

        # Other
        image_name = room["ImageName"]
        description = room["Description"]
        r_date = room["CreatedAt"]

        # Warning
        custom_warning = room["CustomWarning"]
        if custom_warning:
            custom_warning = f"\n**Custom warning**\n```{custom_warning}```"
        else:
            custom_warning = ""
        supported = ""
        if room["SupportsWalkVR"]:
            supported += " 🏃‍♂️ "
        if room["SupportsTeleportVR"]:
            supported += " <:RRtele:803747393769570324> "
        if room["SupportsVRLow"]:
            supported += " <:OQ1:803932601768476672> "
        if room["SupportsQuest2"]:
            supported += " <:OQ2:803932151971577896> "
        if room["SupportsScreens"]:
            supported += " 🖥️ "
        if room["SupportsMobile"]:
            supported += " 📱 "
        if room["SupportsJuniors"]:
            supported += " 👶 "

        # Tags
        tags = ""
        for i in room["Tags"]:
            tags += "#" + str(i["Tag"]) + " "
        if not tags:
            tags = "None"

        # Score
        avg_score = 0
        score_list = []
        for i in room["Scores"]:
            if not i["VisitType"] == 2:
                score_list.append(i["Score"])
                avg_score += i["Score"]
        avg_score = round(avg_score / len(score_list), 5)

        embed=discord.Embed(
            colour=discord.Colour.orange(),
            title = f"Statistics for ^{r_name}, by @{owner_username}",
            description = f"[🔗 RecNet Page](https://rec.net/room/{r_name})\n\n**Description**\n```{description}```{custom_warning}\n**Information**\n:calendar: `{r_date[:10]}` ⏰ `{r_date[11:16]} UTX` *(CREATION DATE)*\n<:CheerHost:803753879497998386> `{role_count}` *(USERS WITH A ROLE)*\n🚪 `{subrooms}` *(SUBROOMS)*\n<:tag:803746052946919434> `{tags}` *(TAGS)*\n\n**Supported modes**\n{supported}\n\n**Statistics**\n<:CheerGeneral:803244099510861885> `{cheers}` *(CHEERS)*\n⭐ `{favorites}` *(FAVORITES)*\n👤 `{visitor_count}` *(VISITORS)*\n👥 `{visit_count}` *(ROOM VISITS)*\n🔥 `#{placement}` *(HOT PLACEMENT)*\n💯 `{avg_score}` *(AVG SCORE)*"
        )
        print("oimg")
        embed.set_image(url=f"https://img.rec.net/{image_name}?width=720")
        
        print("author")
        embed.set_author(name=f"{owner_username}'s profile", url=f"https://rec.net/user/{owner_username}", icon_url=owner_pfp)
        return embed
    else:
        return None

def id_to_room_name(room_id):
    try:
        room_name = requests.get(f"https://api.rec.net/roomserver/rooms/{room_id}").json()['Name']
    except:
        room_name = "DormRoom"
    return room_name

def get_featured_rooms():
    return requests.get("https://api.rec.net/roomserver/featuredrooms/current").json()["Rooms"]

def get_room_score(room_name):
    room = get_room_json(room_name)
    avg_score = 0
    score_list = []
    for i in room["Scores"]:
        if not i["VisitType"] == 2:
            score_list.append(i["Score"])
            avg_score += i["Score"]
    avg_score = round(avg_score / len(score_list), 5)
    return avg_score

def get_frontpage(amount=5):
    frontpage = requests.get(f"https://api.rec.net/api/images/v3/feed/global?take={amount}").json()
    return frontpage

def find_random_bio():
    bio = None
    while bio == None:
        account_id = random.randint(1, 10000000)
        try:
            bio = requests.get(f"https://accounts.rec.net/account/{account_id}/bio").json()["bio"]
        except:
            continue
    return {"account_id": account_id, "bio": bio}

def find_random_account():
    account_id = random.randint(1, 10000000)
    account = None
    while not account:
        try:
            account = requests.get(f"https://accounts.rec.net/account/{account_id}").json()
        except:
            continue
    return account

def find_random_img():
    img_json = None
    while img_json == None:
      random_int = random.randint(1, 18200000)
      img = requests.get(f"https://api.rec.net/api/images/v4/{random_int}")
      if img.ok == False:
            continue
      img_json = img.json()
    return img_json

def find_random_room():
    room = None
    while not room:
        random_int = random.randint(1, 12000000)
        room_data = requests.get(f"https://api.rec.net/roomserver/rooms/{random_int}?include=366")
        if not room_data.ok:
            continue
        else:
            break
    return room_data.json()

def find_random_event():
    events_json = requests.get("https://api.rec.net/api/playerevents/v1?take=1000").json()
    random_int = random.randint(1, len(events_json)-1)
    return events_json[random_int]

def event_search(word):
    events = requests.get(f"https://api.rec.net/api/playerevents/v1/search?query={word}&take=10").json()
    return events

def get_bio(account_id):
    # Get someones bio with their account's id
    return requests.get(f"https://accounts.rec.net/account/{account_id}/bio").json()["bio"]

def embed_footer(ctx, embed):
    today = get_date()
    return embed.set_footer(text=f"Requested by {ctx.author.name} - {today.format('MM/DD/YYYY')}", icon_url=ctx.author.avatar_url)

def contains_word(sentence, word):
    return (' ' + word.casefold() + ' ') in (' ' + sentence.casefold() + ' ')

def error_msg(ctx, desc):
    embed=discord.Embed(
        colour=discord.Colour.orange(),
        description = desc
    )
    embed = embed_footer(ctx, embed)
    return embed

def default_embed():
    return discord.Embed(colour=discord.Colour.orange())