import pymysql
import pymysql.cursors


def phrase_former(phrase: str, sep: str) -> list:
    phrase_list = []
    split_phrase = phrase.split()

    for i in range(len(split_phrase) + 1):
        phrase_list.append(' '.join(split_phrase[:i]) + sep + ' ' + ' '.join(split_phrase[i:]))

    phrase_list.pop()

    return phrase_list[1:]


def search(phrase: str, cursor: pymysql.cursors.Cursor) -> list:
    """
    search for movies using `phrase`
    """

    title_search = []
    cast_search = []
    overview_search = []

    phrase = phrase.strip()

    L = []
    s = ''
    for sep in [':', ';', ' -']:
        L.extend(phrase_former(phrase, sep))
    L.insert(0, phrase)
    for i in L:
        s += f'"%{i}%" or title like '
    s = s[:len(s) - 15]

    cursor.execute(f'select id from main where title sounds like "{phrase}" or title like {s}')
    title_search.extend([int(j[0]) for j in cursor.fetchall()])

    cursor.execute(f'select id from main where cast like "%{phrase}%" order by popularity desc')
    cast_search.extend([int(i[0]) for i in cursor.fetchall()])

    combined_search = title_search + cast_search + overview_search
    result = []
    result = [i for i in combined_search if i not in result]

    return result
