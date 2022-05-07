import re

def getEmojis(input: str):
    foundedEmojis = re.findall("<?(a)?:?(\w{2,32}):(\d{14,20})>", input)
    emojis = []
    json = [{"name": emoji[1], "id": str(emoji[2])} for emoji in foundedEmojis ]
    for emoji in json:
        if not emoji in emojis:
            emojis.append(emoji)
    return emojis