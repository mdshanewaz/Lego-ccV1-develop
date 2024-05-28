import psycopg2
import os
from django.conf import settings




def get_db_conn1():
    conn = False
    try:
        conn = psycopg2.connect(dbname="upel118", user="marking5", password="goodday5", host="tashkent244.czcdn5vf7gyd.us-east-1.rds.amazonaws.com", port='5432')
        print('conn ok')
        conn = True
        if conn == True:
            print('conn true')
        else:
            print('conn false')
        return conn
    except Exception as e:
        print(e)
        return conn



def get_db_conn2():
    conn = psycopg2.connect(dbname="upel118", user="marking5", password="goodday5", host="tashkent244.czcdn5vf7gyd.us-east-1.rds.amazonaws.com", port='5432')
    return conn


# # get_table_conn()
# cont2 = conn45()
# if cont2 != None:
#     print(cont2)
#     print(type(cont2))
# else:
#     print(cont2)
#     print(type(cont2))    




def fetch_order_records(tracking_id, email_add):
    conn = get_db_conn1()
    if conn != None:
        print("conn is NOT none from lin105")
        query2 = """select 
                        rm.title,
                        rm.sku,
                        rm.processing_status,
                        rm.tracking_id , 
                        pm.guest_login_email_address  
                    from resumeweb_mcart rm 
                    inner join resumeweb_mcompleted_purchase pm 
                    on rm.mcompleted_purchase_id = pm.id 
                    where 
                        rm.purchased = true 
                        and rm.tracking_id = %s
                        and pm.guest_login_email_address = %s


            """
        cursor = conn.cursor()
        cursor.execute(query2, (tracking_id, email_add))
        raw_data = cursor.fetchall()
        return raw_data
    else:
        print("something wrong88275")


# fetch_order_records('677-00021-575193', 'tresumccv@gmail.com')
get_db_conn1()
print(conn)
