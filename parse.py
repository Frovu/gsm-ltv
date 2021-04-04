
import sqlite3
conn = sqlite3.connect("gsmltv.db")
cursor = conn.cursor()

def transform_name(cname):
	name = cname.lower().replace(',', '_')
	return ("y_" if cname[0].isdigit() else "") + name

def parse(fname):
	with open(fname) as f:
		lines = f.readlines()[1:]
	return  ([transform_name(c) for c in lines[0].split()],
		[l.split() for l in lines[2:]])

def create_table(columns, rows):
	column_defs = [f"{columns[0]} text"] + [f"{c} real" for c in columns[1:]]
	column_defs = ', '.join(column_defs)
	cursor.execute(f"CREATE TABLE IF NOT EXISTS Rc (\n{column_defs})")
	rows_parsed = [[row[0]] + [float(i) for i in row[1:len(columns)]] for row in rows]
	cursor.executemany(f"INSERT INTO Rc VALUES ({','.join('?'*len(columns))})", rows_parsed)
	conn.commit()



columns, rows = parse("Rc_IGRF.txt")
create_table(columns, rows)
