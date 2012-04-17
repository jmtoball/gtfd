

def fuzzy_delta(delta):
    if type(delta).__name__ != "timedelta":
        return None
    s = delta.seconds
    d = delta.days
    #s = s%(3600 * 24)
    h = round(s / (3600.0))
    s = s % (3600.0)
    m = round(s / (60.0))
    s = round(s % (60.0))
    text = ""
    if d == 0:
        if h == 0:
            if m > 45:
                text = "< 1hr"
            elif m == 0:
                text = "< 1min"
            elif m == 1:
                if s > 20:
                    text = "> 1min"
                else:
                    text = "1min"
            else:
                text = "~" + str(m) + "mins"
        else:
            if h > 20:
                text = "< 1day"
            elif h == 1:
                if m > 20:
                    text = "> 1hr"
                else:
                    text = "1hr"
            else:
                text = "~" + str(h) + "hrs"
    else:
        if h > 5:
            if d > 1:
                text = "> " + str(d) + "days"
            else:
                text = "> 1day"
        else:
            text = "~" + str(d) + "days"
    return text
