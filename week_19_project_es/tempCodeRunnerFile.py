ret = {}
with Image.open("tweet_0.png") as file:
    info = file.getexif()
    for tag, value in info.items():
        decoded = TAGS.get(tag, tag)
        ret[decoded] = value
print(ret)
