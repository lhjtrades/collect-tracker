from flask import Flask
from flask_pymongo import PyMongo

import bcrypt, uuid, secrets

def find_items(item_list, query):
    count = 0
    for dictionary in item_list:
        if dictionary['hidden_status'].lower() == query:
            count+=1

    return count

def clear_type(item_list, user, query):
    item_list.update_many(
        {'username':user}, 
        {'$pull': {'items': {'hidden_status': query}}}
    )