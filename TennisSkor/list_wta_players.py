from collections import OrderedDict
players = [
    {
        "name": "Serena Williams",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/d/d3/Serena_Williams_at_the_2025_International_Tennis_Hall_of_Fame_Induction_Ceremony_Press_Conference_%28cropped%29.jpg",
        "titles": 73,
        "finals": 98,
        "best_ranking": 1,
        "height": 175
    },
    {
        "name": "Steffi Graf",
        "country": "GER",
        "flag": "https://flagcdn.com/w40/de.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Steffi_Graf_in_Hamburg_2010_%28cropped%29.jpg",
        "titles": 107,
        "finals": 144,
        "best_ranking": 1,
        "height": 176
    },
    {
        "name": "Martina Navratilova",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/a/aa/Martina_Navratilova_Eastbourne_2011.jpg",
        "titles": 167,
        "finals": 239,
        "best_ranking": 1,
        "height": 173
    },
    {
        "name": "Chris Evert",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/2/21/Chris_Evert.jpg",
        "titles": 157,
        "finals": 230,
        "best_ranking": 1,
        "height": 168
    },
    {
        "name": "Margaret Court",
        "country": "AUS",
        "flag": "https://flagcdn.com/w40/au.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/1/1b/Margaret_Court.png",
        "titles": 92,
        "finals": 127,
        "best_ranking": 1,
        "height": 175
    },
    {
        "name": "Monica Seles",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/0/08/Monica_Seles_1999.jpg",
        "titles": 53,
        "finals": 68,
        "best_ranking": 1,
        "height": 178
    },
    {
        "name": "Venus Williams",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/1/19/Venus_Williams_%282025_DC_Open%29_crop.jpg",
        "titles": 49,
        "finals": 83,
        "best_ranking": 1,
        "height": 185
    },
    {
        "name": "Justine Henin",
        "country": "BEL",
        "flag": "https://flagcdn.com/w40/be.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/f/fe/Justine_Henin.JPG",
        "titles": 43,
        "finals": 66,
        "best_ranking": 1,
        "height": 167
    },
    {
        "name": "Kim Clijsters",
        "country": "BEL",
        "flag": "https://flagcdn.com/w40/be.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/7/71/Kim_Clijsters.jpg",
        "titles": 41,
        "finals": 60,
        "best_ranking": 1,
        "height": 174
    },
    {
        "name": "Maria Sharapova",
        "country": "RUS",
        "flag": "https://flagcdn.com/w40/ru.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/b/bc/Maria_Sharapova_during_opening_night_of_Web_Summit_2025_at_the_MEO_Arena_in_Lisbon%2C_Portugal.jpg",
        "titles": 36,
        "finals": 59,
        "best_ranking": 1,
        "height": 188
    },
    {
        "name": "Ashleigh Barty",
        "country": "AUS",
        "flag": "https://flagcdn.com/w40/au.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/1/10/Sydney_International_WTA_Players_Cruise_%2831974227527%29_%28cropped_2%29.jpg",
        "titles": 15,
        "finals": 21,
        "best_ranking": 1,
        "height": 166
    },
    {
        "name": "Iga Swiatek",
        "country": "POL",
        "flag": "https://flagcdn.com/w40/pl.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/a/a6/Swiatek_RG19.jpg",
        "titles": 20,
        "finals": 25,
        "best_ranking": 1,
        "height": 176
    },
    {
        "name": "Aryna Sabalenka",
        "country": "BLR",
        "flag": "https://flagcdn.com/w40/by.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/f/f0/Aryna_Sabalenka_%282024_DC_Open%29_06.jpg",
        "titles": 15,
        "finals": 25,
        "best_ranking": 1,
        "height": 182
    },
    {
        "name": "Naomi Osaka",
        "country": "JPN",
        "flag": "https://flagcdn.com/w40/jp.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/d/d6/NaomiOsaka-smile-2020_%28cropped_tight%29.png",
        "titles": 7,
        "finals": 11,
        "best_ranking": 1,
        "height": 180
    },
    {
        "name": "Simona Halep",
        "country": "ROM",
        "flag": "https://flagcdn.com/w40/ro.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/f/f7/Simona_Halep_at_2026_Transylvania_Open.jpg",
        "titles": 24,
        "finals": 42,
        "best_ranking": 1,
        "height": 168
    },
    {
        "name": "Angelique Kerber",
        "country": "GER",
        "flag": "https://flagcdn.com/w40/de.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/f/ff/Australian_Open_2020_%2849836755508%29_%28cropped%29.jpg",
        "titles": 14,
        "finals": 32,
        "best_ranking": 1,
        "height": 173
    },
    {
        "name": "Victoria Azarenka",
        "country": "BLR",
        "flag": "https://flagcdn.com/w40/by.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/6/6c/Victoria_Azarenka_%282024_DC_Open%29_02_%28cropped%29.jpg",
        "titles": 21,
        "finals": 41,
        "best_ranking": 1,
        "height": 183
    },
    {
        "name": "Caroline Wozniacki",
        "country": "DEN",
        "flag": "https://flagcdn.com/w40/dk.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/d/d9/Caroline_Wozniacki_%2835449695422%29.jpg",
        "titles": 30,
        "finals": 55,
        "best_ranking": 1,
        "height": 177
    },
    {
        "name": "Lindsay Davenport",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/4/4c/Davenport_2013_%28cropped%29.jpg",
        "titles": 55,
        "finals": 92,
        "best_ranking": 1,
        "height": 189
    },
    {
        "name": "Jennifer Capriati",
        "country": "USA",
        "flag": "https://flagcdn.com/w40/us.png",
        "photo": "https://upload.wikimedia.org/wikipedia/commons/6/6f/Jennifer_Capriati_Wimbledon_2004.jpg",
        "titles": 14,
        "finals": 31,
        "best_ranking": 1,
        "height": 170
    }
]

players = sorted(players, key=lambda x: x["name"])