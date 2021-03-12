text_arr = ['Distributor', 'Walt Disney Studios Motion Pictures', 'See full company information', '\n', '\n', 'Opening', '$179,139,142', '4,226\n            theaters', 'Budget', '$250,000,000', 'Release Date', 'May 6, 2016', '\n            -\n            ', 'Sep 22, 2016', 'MPAA', 'PG-13', 'Running Time', '2 hr 27 min', 'Genres', 'Action\n    \n        Adventure\n    \n        Sci-Fi', 'In Release', '240 days/34 weeks', 'Widest Release', '4,226 theaters', '\n                        IMDbPro\n                    ', 'See more details at IMDbPro', '\n', '\n']

for i in range(len(text_arr)):
    text_arr[i] = text_arr[i].strip()
    print(i, text_arr[i])

def getInfo(text_arr, field, attr = 1):
    if(field not in text_arr):
        return ":("
    idx = text_arr.index(field)
    # print("------------>>", idx)
    beg = idx + 1
    return text_arr[beg : beg + attr]

def parseGeneralInfo(text_arr):
    info = {}
    info["Distributor"] = getInfo(text_arr, "Distributor")[0]
    info["Opening"] = getInfo(text_arr, "Opening")[0]
    info["Budget"] = getInfo(text_arr, "Budget")[0]
    info["Release Date"] = getInfo(text_arr, "Release Date", 3)
    info["MPAA"] = getInfo(text_arr, "MPAA")[0]
    genres = getInfo(text_arr, "Genres")[0].split()
    for i in range(len(genres)):
        genres[i] = genres[i].strip()
    info["Genres"] = genres
    info["In Release"] = getInfo(text_arr, "In Release")[0]
    info["Widest Release"] = getInfo(text_arr, "Opening")[0]

    return info

print(parseGeneralInfo(text_arr))