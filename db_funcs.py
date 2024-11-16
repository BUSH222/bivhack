from dbloader import connect_to_db

conn, cur = connect_to_db()


def create_new_field(name,desc,var_type,formula,hidden,edit):
    '''
    Creates a new field
        Args:
            - name (str): The name of a field.
            - var_type (int): 0: string, 1: number (int/float), 2: boolean .
            - formula (str): We still dont really know how to store\use this.
            - hidden (bool): Not shown to user.
            - edit (bool): Can be edited by admin
        Returns:
            - field id that was created
    '''
    cur.execute("INSERT INTO field ( var_name, description,variable_type,variable_formula,default_value,hidden,editable) VALUES (%s,%s,%s,%s,%s,%s) RETURNING id",
                (name,desc,var_type,formula, hidden,edit))
    s_id = cur.fetchone()
    return s_id


def create_insurance_from_template(ins_id:int,fields:dict,new_ins_name:str,new_ins_desc:str,signable:bool):
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
    cur.execute('''SELECT * FROM insurance_product_fields WHERE insurance_product_id = %s''',(ins_id))
    inherited_fields = cur.fetchall()

    cur.execute('''INSERT INTO insurance_products (name,description,signable) VALUES (%s,%s,%s) RETURNING id''',(new_ins_name,new_ins_desc,signable))
    new_ins_id = cur.fetchone()
    for row in inherited_fields:
        cur.execute('''INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES(%s,%s)''',new_ins_id,row[2])
    for field in fields:
        cur.execute('''INSERT INTO insurance_product_fields (insurance_product_id, field_id) VALUES(%s,%s)''',new_ins_id,create_new_field(field['name'],field['desc'],field['var_type'],field['formula'],field['hidden'],field['edit']))
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
            cur.execute("UPDATE fields SET var_name = %s, description = %s,variable_type = %s,variable_formula = %s,default_value = %s,hidden = %s,editable = %s WHERE id = %s",
                        (field["var_name"],field["description"],field["variable_type"],field["variable_formula"],field["default_value"],field["hidden"],field["editable"],field["id"]))
        try:
            conn.commit()
        except Exception:
            conn.rollback()


def create_contract(insurance_product_id,fields):
        '''
        Creates contract from any insurance product. Expects insurance product id and set of dicts that are tagged according to fields formation.
        
        Args:
            -fields_edits (dict): set of dicts of fields with changed values. It's enought cuz each element contains field id
        Returns:
            - nill
        '''
