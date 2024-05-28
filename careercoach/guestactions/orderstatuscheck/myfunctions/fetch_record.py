import psycopg2
import os
import time
import json
from pprint import pprint

from django.conf import settings
# from django.core.cache import cache
from dbops.db_conn import get_db_conn1


# fetch order_info function updated 03/22/2023
##***********************************************
def fetch_record_orderinfo(conn,tracking_id):
    # print(end_date)

    query5 = """select
                    rm.processing_status, 
                    rm.tracking_id
                from resumeweb_mcart rm
                inner join resumeweb_mcompleted_purchase pm
                on rm.mcompleted_purchase_id = pm.id 
                where 
                    rm.purchased = true and
                    rm.tracking_id = %s"""

    cursor = conn.cursor()
    # start = time.time()
    cursor.execute(query5, (tracking_id,))

    order_data = cursor.fetchall()
    # end = time.time()
    # print("\nquery exec time:", end-start)
    # print(raw_data)

    return order_data


# fetch buyer_info function updated 03/22/2023
##***********************************************
def fetch_record_buyerinfo(conn,email_add):
    # conn = get_db_conn1()
    # print('nothing wrong here line104')

    query4 = """select rm.email
                from resumeweb_buyerlistguest rm
                where rm.email = %s;"""

    cursor = conn.cursor()
    # start = time.time()
    cursor.execute(query4, (email_add,))
    # cursor.execute(query1)
    buyer_data = cursor.fetchall()
    # end = time.time()
    # print("\nquery exec time:", end-start)
    # print(raw_data)

    return buyer_data
