from resumeweb.models import (
    mcart,
)
import psycopg2
import os
from django.conf import settings



def search_order_data_v0(tracking_id, email_add):

    p = mcart.objects.get(tracking_id=tracking_id, muser__email=email_add)

    return p


def get_db_conn1():
    conn = psycopg2.connect(
        dbname =    os.environ.get("RESUMEWEB_DBNAME"),
        user =      os.environ.get("RESUMEWEB_DBUSERNAME"),
        password =  os.environ.get("RESUMEWEB_DBPASS"),
        host =      os.environ.get("RESUMEWEB_DBHOST"),
        port =      os.environ.get("port"),

    )

    return conn


def get_db_conn2():
    conn = psycopg2.connect(dbname="upel118", user="barking5", password="goodday5", host="tashkent244.czcdn5vf7gyd.us-east-1.rds.amazonaws.com", port='5432')
    return conn


def fetch_order_records_test():
    conn = get_db_conn1()

    if conn != None:
        query3 = """select 
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
                    and rm.tracking_id = '677-00021-575193'
                    and pm.guest_login_email_address = 'tresumccv@gmail.com';

        """
        cursor = conn.cursor()
        cursor.execute(query3)
        raw_data = cursor.fetchall()

        if len(raw_data) > 0:
            return raw_data
        else:
            return False
    else:
        return None




def fetch_order_records_v0(tracking_id, email_add):
    conn = ''
    try:
        conn = get_db_conn1()
        if conn != None:
            print("conn is NOT none from line61")
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

            if len(raw_data) > 0:
                return raw_data
            else:
                return False
        else:
            return None
    except Exception as e:
        print(e)
    finally:
        if (conn):
            cursor.close()
            conn.close()




# this function worked just fine
def fetch_order_records(tracking_id):
    conn = get_db_conn1()
    print('nothing wrong here line104')
    print(tracking_id)
    query1 = """select 
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
                    ;
        """

    query2 = "select * from resumeweb_mcart rm where rm.tracking_id = %s;"
    cursor = conn.cursor()
    cursor.execute(query2, (tracking_id,))
    raw_data = cursor.fetchall()
    print(raw_data)
    return raw_data

