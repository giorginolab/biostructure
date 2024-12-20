'''
Created on 22 feb. 2019

@author: luis98
'''
from psycopg2 import sql
import json

class Descriptor(object):
    '''
    classdocs
    '''
    __emd_entry_id = None
    __type_descriptor_id = None
    __numbers = None

    def __init__(self, emd_entry_id, type_descriptor_id, numbers):
        self.__emd_entry_id = emd_entry_id
        self.__type_descriptor_id = type_descriptor_id
        self.__numbers = numbers

    def insert_db(self, cur):
        cur.execute(
            sql.SQL("INSERT INTO descriptor(emd_entry_id,type_descriptor_id,numbers) VALUES (%s,%s,%s);"), [
                self.__emd_entry_id, self.__type_descriptor_id, json.dumps(
                    self.__numbers)])

    def update_db(self, cur):
        cur.execute(
            sql.SQL("UPDATE descriptor SET numbers = %s WHERE emd_entry_id = %s and type_descriptor_id = %s;"), [
                json.dumps(
                    self.__numbers), self.__emd_entry_id, self.__type_descriptor_id])
        
    def insert_update_db(self, cur):
        cur.execute(
            sql.SQL("SELECT numbers FROM descriptor WHERE emd_entry_id = %s and type_descriptor_id = %s;"),[
                self.__emd_entry_id, self.__type_descriptor_id])
        result = [record[0] for record in cur]
        if len(result)>0:
            self.update_db(cur)
        else:
            self.insert_db(cur)

    def get_emd_entry_id(self):
        return self.__emd_entry_id

    def get_type_descriptor_id(self):
        return self.__type_descriptor_id

    def get_numbers(self):
        return self.__numbers

    def set_emd_entry_id(self, value):
        self.__emd_entry_id = value

    def set_type_descriptor_id(self, value):
        self.__type_descriptor_id = value

    def set_numbers(self, value):
        self.__numbers = value

    def del_emd_entry_id(self):
        del self.__emd_entry_id

    def del_type_descriptor_id(self):
        del self.__type_descriptor_id

    def del_numbers(self):
        del self.__numbers

    def __eq__(self, descriptor):
        return self.emd_entry_id == descriptor.emd_entry_id \
            and self.type_descriptor_id == descriptor.type_descriptor_id \
            and self.numbers == descriptor.numbers

    emd_entry_id = property(
        get_emd_entry_id,
        set_emd_entry_id,
        del_emd_entry_id,
        "emd_entry_id's docstring")
    type_descriptor_id = property(
        get_type_descriptor_id,
        set_type_descriptor_id,
        del_type_descriptor_id,
        "type_descriptor_id's docstring")
    numbers = property(
        get_numbers,
        set_numbers,
        del_numbers,
        "numbers's docstring")
