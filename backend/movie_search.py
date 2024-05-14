import pymysql
import pymysql.cursors


def phrase_former(phrase: str, sep: str) -> list[str]:
    """
    forms phrase for searching movies
    """
    phrase_list = []
    split_phrase = phrase.split()

    for i in range(len(split_phrase) + 1):
        phrase_list.append(' '.join(split_phrase[:i]) + sep + ' ' + ' '.join(split_phrase[i:]))

    phrase_list.pop()

    return phrase_list[1:]


def search(phrase: str, cursor: pymysql.cursors.Cursor) -> list[int]:
    """
    search for movies using `phrase`
    """

    title_search = []
    cast_search = []
    # overview_search = []
    prod_search = []

    phrase = phrase.strip()

    L = []
    s_title = ''
    s_cast = ''
    s_prod = ''
    for sep in [':', ';', ' -']:
        L.extend(phrase_former(phrase, sep))
    L.insert(0, phrase)
    for i in L:
        s_title += f'"%{i}%" or title like '
        s_cast +=  f'"%{i}%" or cast like '
        s_prod +=  f'"%{i}%" or production_companies like '
    s_title = s_title[:len(s_title) - 15]
    s_cast = s_cast[:len(s_cast) - 14]
    s_prod = s_prod[:len(s_prod) - 30]

    cursor.execute(f'select id from main where title = "{phrase}" or title like "%{phrase}%" or title sounds like "{phrase}" or title like {s_title} order by popularity desc')
    title_search.extend([int(j[0]) for j in cursor.fetchall()])

    cursor.execute(f'select id from main where cast like {s_cast}')
    cast_search.extend([int(j[0]) for j in cursor.fetchall()])

    cursor.execute(f'select id from main where production_companies like {s_prod}')
    prod_search.extend([int(j[0]) for j in cursor.fetchall()])

    # cursor.execute(f'select id from main where cast like "%{phrase}%" order by popularity desc')
    # cast_search.extend([int(i[0]) for i in cursor.fetchall()])


    combined_search = title_search + cast_search + prod_search
    result = []
    result = [i for i in combined_search if i not in result]

    return result
