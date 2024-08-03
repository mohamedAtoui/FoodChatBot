import mysql.connector
global cnx
cnx= mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='pandeyji_eatery'
    )
def get_order_status(order_id:int):
    
    cursor=cnx.cursor()
    
    query=("SELECT status FROM pandeyji_eatery.order_tracking WHERE order_id=%s")
    
    cursor.execute(query,(order_id,))
    
    result = cursor.fetchone()
    
    
    
    
    if result is not None:
        return result[0]
    else:
        return None

def get_next_order_id():
    cursor=cnx.cursor()
    
    query="SELECT MAX(order_id) FROM pandeyji_eatery.orders"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    print(result)
    cursor.close()
    
    if result is None:
        return 1
    else:
        return result+1
def insert_order_tracking(order_id, status):
    cursor=cnx.cursor()
    
    insert_query="INSERT INTO pandeyji_eatery.order_tracking (order_id, status) VALUES (%s, %s)"
    cursor.execute(insert_query,(order_id,status))
    cnx.commit()
    
def insert_order_item(food_item,quantity, oreder_id):
    try:
        cursor=cnx.cursor()
        
        cursor.callproc('insert_order_item',(food_item,quantity,oreder_id))
        
        cnx.commit()
        
        print("order item inserted")
        
        return 1
    
    except Exception as e:
        print('exception')
        cnx.rollback()
        return -1
    
    
def get_total_order_price(order_id):
    cursor=cnx.cursor()
    
    query=f"SELECT get_total_order_price({order_id})"
    cursor.execute(query)
    result=cursor.fetchone()[0]
    return result
        
    