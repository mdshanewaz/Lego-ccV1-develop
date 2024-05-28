# from resumeweb.models import (
#     mcart,
# )
# import psycopg2
# import os
# import time
# import json
# from pprint import pprint

# from django.conf import settings
# from django.core.cache import cache


# # step-1: fetch emails from auth_user table
# # step-2: save data from raw_data_email_list
# # step-3: print raw_data_list 
# ##******************************************************************************
# def read_from_redis_cache(raw_data_email_list):
#     # raw_data_list = list(set(raw_data_email_list))
#     raw_data_list = [('ariful1@gmail.com',),('ariful2@gmail.com',)]
 
#     # print(raw_data_list)
#     raw_data_list = [x[0] for x in raw_data_list]
#     raw_data_dict = { i : i for i in raw_data_list }
#     cache.set("data_dict", json.dumps(raw_data_dict))
#     pprint(json.loads(cache.get("data_dict")))
#     if len(raw_data_dict)> 0 and raw_data_email_list in cache.get("data_dict"):
#         if json.loads(cache.get("data_dict")):
#             print(cache.keys('*'))
#             return json.loads(cache.get("data_dict"))
#         return True 

#     else:
#         return False

# # step-1: fetch emails from auth_user table
# # step-2: save data from raw_data_email_list
# # step-3: print raw_data_list 
# ##******************************************************************************
# def read_from_redis_cache(raw_data_email_list):
#     # raw_data_list = list(set(raw_data_email_list))
#     raw_data_list = [('ariful1@gmail.com',),('ariful2@gmail.com',)]
 
#     # print(raw_data_list)
#     raw_data_list = [x[0] for x in raw_data_list]
#     raw_data_dict = { i : i for i in raw_data_list }
#     cache.set("data_dict", json.dumps(raw_data_dict))
#     pprint(json.loads(cache.get("data_dict")))
#     if len(raw_data_dict)> 0 and raw_data_email_list in cache.get("data_dict"):
#         if json.loads(cache.get("data_dict")):
#             print(cache.keys('*'))
#             return json.loads(cache.get("data_dict"))
#         return True 

#     else:
#         return False


