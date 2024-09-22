
def createAlias(url, time):
    time_str = time.isoformat()
    holder = url+time_str
    holder = hash(holder)
    return str(holder)[:5]