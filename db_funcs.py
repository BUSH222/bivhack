from dbloader import connect_to_db

conn, cur = connect_to_db()
def create_new_field(name,desc,var_type,formula,hidden,edit):
    '''
    Creates new field
     Args:
            - name (str): The name of a field.
            - var_type (int): 0: string, 1: number (int/float), 2: boolean .
            - formula (str): We still dont really know how to store\use this.
            - hidden (bool): Not shown to user.
            - edit (bool): Can be eddited by admin
    '''
    cur.execute("INSERT INTO field ( var_name, description,variable_type,variable_formula,default_value,hidden,editable) VALUES (%s,%s,%s,%s,%s,%s)",
                (name,desc,var_type,formula, hidden,edit))

    


def create_insurance_from_template(ins_id:int,fields:dict,new_ins_name:str,new_ins_desc:str):
    
    cur.execute('''SELECT * FROM insurance_product_fields WHERE insurance_product_id = %s''',(ins_id))
    inherited_fields = cur.fetchall()

    cur.execute('''INSERT INTO insurance_products (name,description) VALUES (%s,%s) RETURNING id''',(new_ins_name,new_ins_desc))
    new_ins_id = cur.fetchone()
    for id
    creation_querry = f'INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES('
    
def modify_insurance_form(table_name:str):
    