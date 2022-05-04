def change_time_temp(hour, room):
    match hour:
        case 0:
            return 17.2 + rooms_factor(room, hour)
        case 1:
            return 16.8 + rooms_factor(room, hour)
        case 2:
            return 16.5 + rooms_factor(room, hour)
        case 3:
            return 15.9 + rooms_factor(room, hour)
        case 4:
            return 15.9 + rooms_factor(room, hour)
        case 5:
            return 15.6 + rooms_factor(room, hour)
        case 6:
            return 15 + rooms_factor(room, hour)
        case 7:
            return 15.2 + rooms_factor(room, hour)
        case 8:
            return 16.9 + rooms_factor(room, hour)
        case 9:
            return 18.6 + rooms_factor(room, hour)
        case 10:
            return 20.5 + rooms_factor(room, hour)
        case 11:
            return 22.1 + rooms_factor(room, hour)
        case 12:
            return 23.2 + rooms_factor(room, hour)
        case 13:
            return 23.6 + rooms_factor(room, hour)
        case 14:
            return 23.3 + rooms_factor(room, hour)
        case 15:
            return 23.6 + rooms_factor(room, hour)
        case 16:
            return 23.5 + rooms_factor(room, hour)
        case 17:
            return 22.8 + rooms_factor(room, hour)
        case 18:
            return 21.7 + rooms_factor(room, hour)
        case 19:
            return 20.5 + rooms_factor(room, hour)
        case 20:
            return 19.1 + rooms_factor(room, hour)
        case 21:
            return 18.5 + rooms_factor(room, hour)
        case 22:
            return 17.9 + rooms_factor(room, hour)
        case 23:
            return 17.2 + rooms_factor(room, hour)


def rooms_factor(room, hour):
    match room:
        case 'kitchen':
            if 11 < hour < 16:
                return 2.5
            elif 9 < hour <= 11:
                return 2
            elif 16 <= hour <= 18:
                return 2
            else:
                return 1.5
        case 'bedroom1':
            if 11 < hour < 16:
                return 2
            elif 9 < hour <= 11:
                return 1.5
            elif 16 <= hour <= 18:
                return 1.5
            else:
                return 1
        case 'bedroom2':
            return 1
        case 'bedroom3':
            return 0
        case 'bathroom':
            if 18 < hour < 22:
                return 3.7
            elif 22 <= hour <= 00:
                return 3.2
            elif 9 <= hour <= 18:
                return 2.7
            else:
                return 2.2


