import os
import sys
from calendar import Calendar
from collections import defaultdict
from datetime import date, timedelta

import pandas as pd
import plotly.figure_factory as ff
import requests
from discord_webhook import DiscordEmbed, DiscordWebhook

def get_json(url, params, headers={"x-nxopen-api-key": os.environ["API_KEY"]}):
    response = requests.get(url, params, headers=headers)
    json = response.json()

    if response.status_code == 200:
        return json
    else:
        embed = DiscordEmbed(
            "error",
            "\n".join(f"{k}: {v}" for k, v in json["error"].items())
        )
        webhook.remove_embeds()
        webhook.add_embed(embed)
        webhook.execute()

        sys.exit()

guild_name = "치즈"
avatar_url = "https://raw.githubusercontent.com/hhykim/cheese/main/avatar.png"

webhook = DiscordWebhook(
    os.environ["WEBHOOK_URL"],
    username=guild_name,
    avatar_url=avatar_url,
    rate_limit_retry=True
)

month, week = 0, 0

yesterday = date.today() - timedelta(1)
cal = Calendar().monthdayscalendar(yesterday.year, yesterday.month)

for i, v in enumerate(cal):
    if yesterday.day in v:
        if v[0] == 0:
            yesterday = yesterday - timedelta(7)
            cal = Calendar().monthdayscalendar(yesterday.year, yesterday.month)

            if cal[0][0] == 0:
                week = len(cal) - 1
            else:
                week = len(cal)
        else:
            if cal[0][0] == 0:
                week = i
            else:
                week = i + 1

        month = yesterday.month
        break

embed = DiscordEmbed(
    f"길드 랭킹 ({month}월 {week}주차)",
    color="58b9ff"
)
embed.set_footer("Data based on NEXON Open API")

# 길드 식별자
world_name = "스카니아"
url = "https://open.api.nexon.com/maplestory/v1"

params = {
    "guild_name": guild_name,
    "world_name": world_name
}
json = get_json(f"{url}/guild/id", params)

oguild_id = json["oguild_id"]

# 길드원 수
yesterday = (date.today() - timedelta(1)).strftime("%Y-%m-%d")

params = {
    "oguild_id": oguild_id,
    "date": yesterday
}
json = get_json(f"{url}/guild/basic", params)

guild_member_count = json["guild_member_count"]

embed.add_embed_field(
    "길드원",
    f"{guild_member_count}/200명"
)

# 플래그 레이스
today = date.today().strftime("%Y-%m-%d")

params = {
    "date": today,
    "world_name": world_name,
    "ranking_type": 1,
    "guild_name": guild_name
}
json = get_json(f"{url}/ranking/guild", params)

snowfields = ["한낮", "석양", "한밤"]
index = (date.today() - date(2023, 12, 18)).days // 7 % 3

ranking = json["ranking"][0]["ranking"]
guild_point = json["ranking"][0]["guild_point"]

embed.add_embed_field(
    f"플래그 레이스 - {snowfields[index]}",
    f"{ranking:,}위 ({guild_point:,}점)",
    inline=False
)

# 지하 수로
params["ranking_type"] = 2
json = get_json(f"{url}/ranking/guild", params)

ranking = json["ranking"][0]["ranking"]
guild_point = json["ranking"][0]["guild_point"]

embed.add_embed_field(
    "지하 수로",
    f"{ranking:,}위 ({guild_point:,}점)",
    inline=False
)
embed.fields[1], embed.fields[2] = embed.fields[2], embed.fields[1]
webhook.add_embed(embed)

def get_df(json, start, stop):
    data = defaultdict(list)
    for d in json["ranking"][start:stop]:
        data["순위"].append(d["ranking"])
        data["길드명"].append(d["guild_name"])
        data["점수"].append(f"{d['guild_point']:,}")

    for i, v in enumerate(data["길드명"]):
        if v == guild_name:
            data["순위"][i] = f"** {data['순위'][i]} **"
            break

    return pd.DataFrame(data)

del params["guild_name"]
json = get_json(f"{url}/ranking/guild", params)

for i in range(2):
    df = get_df(json, i * 10, (i + 1) * 10)

    fig = ff.create_table(df, height_constant=18)
    fig.update_layout(width=245)
    fig.write_image(f"{i + 1}.png")

for i in range(2):
    with open(f"{i + 1}.png", "rb") as f:
        webhook.add_file(f.read(), f"{i + 1}.png")
webhook.execute()
