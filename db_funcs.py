from dbloader import connect_to_db

conn, cur = connect_to_db()

def create_insurance_from_template(table_name):
    