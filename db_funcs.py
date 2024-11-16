from dbloader import connect_to_db
import os
import psycopg2

conn, cur = connect_to_db()


def create_new_field(name, desc, var_type, formula, hidden, edit):
    """
    Creates a new field
    Args:
        - name (str): The name of a field.
        - var_type (int): 0: string, 1: number (int/float), 2: boolean .
        - formula (str): We still dont really know how to store \\ use this.
        - hidden (bool): Not shown to user.
        - edit (bool): Can be edited by admin
    Returns:
        - field id that was created
    """
    cur.execute(
        "INSERT INTO field ( var_name, description,variable_type,variable_formula,default_value,hidden,editable) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
        (name, desc, var_type, formula, hidden, edit))
    s_id = cur.fetchone()
    return s_id


def get_insurance_product_info(ins_id: int):
    cur.execute("SELECT field_id FROM insurance_product_fields WHERE insurance_product_id=%s", (ins_id))
    fields_ids = cur.fetchall()
    res = []
    for id in fields_ids:
        cur.execute("SELECT * FROM fields WHERE id = %s", (id))
        info = cur.fetchall()
        res.append(info)
    return res


# def copy_insurance_from_template(ins_id:int):
#    cur.execute('''
#            DO $$
#            DECLARE
#                product_prop RECORD;
#                new_id INTEGER;
#            BEGIN
#                -- Найти продукт по заданному id и сохранить данные в переменную
#                SELECT * INTO product_prop FROM insurance_products WHERE id = %s;
#
#                -- Вставить новый продукт с копированием данных и получить новый id
#                INSERT INTO insurance_products (name, description, signable)
#                VALUES (product_prop.name || '_copy', product_prop.description, product_prop.signable)
#                RETURNING id INTO new_id;
#
#                -- Копировать связанные записи из insurance_product_fields
#                INSERT INTO insurance_product_fields (insurance_product_id, field_id)
#                SELECT new_id, field_id
#                FROM insurance_product_fields
#                WHERE insurance_product_id = %s;
#
#                -- Возврат нового id
#                RETURN new_id;
#            END $$;
#            ''', (ins_id, ins_id))
#    try:
#        conn.commit()
#    except Exception:
#        conn.rollback()
#    new_id = cur.fetchone()[0]
#    return new_id

# def add_fields_in_template(ins_id:int):
#     try:
#         conn.commit()
#     except Exception:
#         conn.rollback()


def create_insurance_from_template(ins_id: int, fields: list, new_ins_name: str, new_ins_desc: str, signable: bool):
    '''
    Inherits field ids from parent and creates new fields from user input
    Creates new insurance product via filling insurance_product_fields table with rows of id of a new insurance_product and coherant field ids for each row

        Args:
            - ins_id (int): id of parent insurance product from which inherits field ids.
            - fields (dict): user input for new fields .
            - new_ins_name (str): name of a new insurance product.
            - new_ins_desc (str): desc of a new insurance product.
            - signable (bool): either contract is abstract and just for creating following ones or the one that can be used by user
        Returns:
            - nill
    '''
    cur.execute('''SELECT * FROM insurance_product_fields WHERE insurance_product_id = %s''', (ins_id))
    inherited_fields = cur.fetchall()

    cur.execute('''INSERT INTO insurance_products (name,description,signable) VALUES (%s,%s,%s) RETURNING id''',
                (new_ins_name, new_ins_desc, signable))
    new_ins_id = cur.fetchone()
    for row in inherited_fields:
        cur.execute('''INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES(%s,%s)''',
                    new_ins_id, row[2])
    for field in fields:
        cur.execute('''INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES(%s,%s)''',
                    new_ins_id,
                    create_new_field(field['var_name'], field['description'], field['variable_type'], field['variable_formula'],field['default_value '],
                                    field['hidden'],
                                    field['edit']))
    try:
        conn.commit()
    except Exception:
        conn.rollback()


def modify_insurance_prodcut_fields(fields_edits):
    '''
    Edits insurance_prodcut_fields, so all those fields are changed in all insurance products. I do expect that frontend returns all params
    filled, becouse I expect that editing page is field with existing info, which is, if not edited, returns with info that was updated
    Args:
        -fields_edits (dict): set of dicts of fields with changed values. It's enought cuz each element contains field id
    Returns:
        - nill
    '''
    for field in fields_edits:
        cur.execute(
            "UPDATE fields SET var_name = %s, description = %s,variable_type = %s,variable_formula = %s,default_value = %s,hidden = %s,editable = %s WHERE id = %s",
            (field["var_name"], field["description"], field["variable_type"], field["variable_formula"],
             field["default_value"], field["hidden"], field["editable"], field["id"]))
    try:
        conn.commit()
    except Exception:
        conn.rollback()


def create_contract(user_id: int, insurance_product_id: int, fields: dict, signature_id_on_server: int = 123):
    '''
    Creates contract from any insurance product. Expects insurance product id and set of dicts that are tagged according to fields formation.
    The contract itself is just header info whith stash of jsons that are {field_id:info} essentially
    Args:
        -user_id(int):selfexplanatory
        -fields(dict):info in dicts for each field.
        -insurance_product_id(int): selfexplanatory
        -signature_id_on_server(int): unique id for each signature saved on server. Use it to load a sig pic from folder into bd
    Returns:
        - nill
    '''
    try:
        with open(os.path.join('static', 'signatures', str(signature_id_on_server))) as pic:
            img_data = pic.read()

    except Exception:
        with open(os.path.join(os.path.join('static', 'signatures'), 'default')) as pic:
            img_data = pic.read()
    reformed_data_dict = {}
    for field in fields:
        reformed_data_dict[field['id']] = field.pop('id')
    cur.execute(
        "INSERT INTO contracts (user_id ,insurance_product_id, insurance_product_data, signatures, created_at) VALUES(%s,%s,%s,%s,CURRENT_TIMESTAMP)",
        (user_id, insurance_product_id, reformed_data_dict, psycopg2.Binary(img_data)))
    try:
        os.remove(os.path.join(os.path.join('static', 'signatures'), str(signature_id_on_server)))
    except Exception:
        print(
            "Failed deleting signature from server hash folder. Probably it wasn't there becouse user didn't load it or some server problem")


def display_insurance_products(filter=None):
    '''
    Returns a heap of json dicts that will be displayed in the frontend. Can be filtered for basic categories such as property, health etc.
        Args:
            -filter: categories filter for returning info.
        Returns:
            - dict of tuples. Keys are names of insurance products
    '''
    result_info_heap = {}
    if filter is not None:
        cur.execute('SELECT * FROM insurance_product_fields')
        insurance_products_fields_ids = cur.fetchall()

        id_fid = {}
        for key, value in insurance_products_fields_ids:
            if key in id_fid:
                id_fid[key].append(value)
            else:
                id_fid[key] = [value]
        for key in id_fid.keys():
            cur.execute('SELECT name FROM insurance_products where id = %s', (key))
            name = cur.fetchone()
            result_info_heap[name] = []
            for field in id_fid[key]:
                cur.execute('SELECT * FROM fields WHERE id=%s', (field))
                current_contract_fields = cur.fetchall()
                result_info_heap[name].append(current_contract_fields)
    else:
        cur.execute("SELECT id FROM insurance_product_categories WHERE name = %s", (filter))
        cat_id = cur.fetchone()
        cur.execute(
            "SELECT insurance_product_id FROM insurance_product_categories_connections WHERE insurance_product_category_id = %s", 
            (cat_id))
        insurance_products_selected = cur.fetchall()
        for insurance_product_id in insurance_products_selected:
            cur.execute('SELECT * FROM insurance_product_fields WHERE insurance_product_id = %s',
                        (insurance_product_id))
            insurance_products_fields_ids = cur.fetchall()
            id_fid = {}
            for key, value in insurance_products_fields_ids:
                if key in id_fid:
                    id_fid[key].append(value)
                else:
                    id_fid[key] = [value]
            for key in id_fid.keys():
                cur.execute('SELECT name FROM insurance_products where id = %s', (key))
                name = cur.fetchone()
                result_info_heap[name] = []
                for field in id_fid[key]:
                    cur.execute('SELECT * FROM fields WHERE id=%s', (field))
                    current_contract_fields = cur.fetchall()
                    result_info_heap[name].append(current_contract_fields)
    return result_info_heap
