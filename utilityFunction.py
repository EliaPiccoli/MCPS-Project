def change_time_temp(hour, room):
    if hour == 0:
        return 17.2 + rooms_factor(room, hour)
    elif hour == 1:
        return 16.8 + rooms_factor(room, hour)
    elif hour == 2:
        return 16.5 + rooms_factor(room, hour)
    elif hour == 3:
        return 15.9 + rooms_factor(room, hour)
    elif hour == 4:
        return 15.9 + rooms_factor(room, hour)
    elif hour == 5:
        return 15.6 + rooms_factor(room, hour)
    elif hour == 6:
        return 15 + rooms_factor(room, hour)
    elif hour == 7:
        return 15.2 + rooms_factor(room, hour)
    elif hour == 8:
        return 16.9 + rooms_factor(room, hour)
    elif hour == 9:
        return 18.6 + rooms_factor(room, hour)
    elif hour == 10:
        return 20.5 + rooms_factor(room, hour)
    elif hour == 11:
        return 22.1 + rooms_factor(room, hour)
    elif hour == 12:
        return 23.2 + rooms_factor(room, hour)
    elif hour == 13:
        return 23.6 + rooms_factor(room, hour)
    elif hour ==  14:
        return 23.3 + rooms_factor(room, hour)
    elif hour == 15:
        return 23.6 + rooms_factor(room, hour)
    elif hour == 16:
        return 23.5 + rooms_factor(room, hour)
    elif hour == 17:
        return 22.8 + rooms_factor(room, hour)
    elif hour == 18:
        return 21.7 + rooms_factor(room, hour)
    elif hour == 19:
        return 20.5 + rooms_factor(room, hour)
    elif hour == 20:
        return 19.1 + rooms_factor(room, hour)
    elif hour == 21:
        return 18.5 + rooms_factor(room, hour)
    elif hour == 22:
        return 17.9 + rooms_factor(room, hour)
    elif hour == 23:
        return 17.2 + rooms_factor(room, hour)


def rooms_factor(room, hour):
    if room == 'kitchen':
        if 11 < hour < 16:
            return 2.5
        elif 9 < hour <= 11:
            return 2
        elif 16 <= hour <= 18:
            return 2
        else:
            return 1.5
    elif room == 'bedroom1':
        if 11 < hour < 16:
            return 2
        elif 9 < hour <= 11:
            return 1.5
        elif 16 <= hour <= 18:
            return 1.5
        else:
            return 1
    elif room == 'bedroom2':
        return 1
    elif room == 'bedroom3':
        return 0
    elif room == 'bathroom':
        if 18 < hour < 22:
            return 3.7
        elif 22 <= hour <= 00:
            return 3.2
        elif 9 <= hour <= 18:
            return 2.7
        else:
            return 2.2