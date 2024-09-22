
def createAlias(url, time):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S")
    holder = url+time_str
    holder = hash(holder)
    return str(holder)[:5]