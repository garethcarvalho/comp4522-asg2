import sqlite3

def create_table_from_csv(cursor: sqlite3.Cursor, tablename: str, types: list) -> None:
    '''
    Creates a table and populates it from a .csv file
    specified by `tablename`. The path to the .csv file will be
    "relations/<`tablename`>.csv"
    '''
    data = []

    # Read the .csv file line-by-line.
    with open(f'relations/{tablename}.csv', 'r') as csv_str:
        line = csv_str.readline()
        while line != '':
            line = line.strip().split(',')
            data.append(line)
            line = csv_str.readline()
    
    cols = data.pop(0);
    cols_str = ''
    size = len(cols)
    for i in range(size):
        cols_str += f'{cols[i]} {types[i]}'
        if (i + 1 < size):
            cols_str += ', '

    # Dropping the table if it already exists for the purposes of this
    # assignment. I understand in scenarios where we care about the persistence of this
    # data, we wouldn't do this.
    query = f'DROP TABLE IF EXISTS {tablename};'
    cursor.execute(query)

    query = f'CREATE TABLE {tablename} ({cols_str});'
    cursor.execute(query)

    for d in data:
        values = tuple(d).__str__() if len(d) > 1 else f"('{d[0]}')"
        query = f'INSERT INTO {tablename} VALUES {values}'
        cursor.execute(query);