import mysql.connector
import configparser
import os
from mysql.connector import Error
from flask import Blueprint


def service_db_config(conf_name='service.conf'):
        '''
        Func to assign data to the db using configParser

        Argument:
            conf_name --- name of the config file including .conf

        Returns:
            complete json variable including 'host', 'user', 'password' and 'database' info
        '''
     #relative path to the service database config
        config_path = os.path.join(os.path.dirname(__file__), '..', 'conf', conf_name)
        #reading the database config
        config = configparser.ConfigParser()
        config.read(config_path)

        
        config_name = conf_name.split('.')
        serviceDB_config = {
        'host': config.get(config_name[0], 'sql-server'),
        'user': config.get(config_name[0], 'sql-user'),
        'password': config.get(config_name[0], 'sql-pass'),
        'database': config.get(config_name[0], 'sql-database')
        }

        return serviceDB_config

def commit_query(query, conf_name):
    '''
        Func to execute, fetch and commit queries like SELECT

        Opens connection to the database, performs fetch then closes the connection

        Returns:
            If True returns all data from query

            If it fails returns 'None'

    '''

    try:
       
        serviceDB = mysql.connector.connect(**service_db_config(conf_name))

        if(serviceDB.is_connected()):
            serviceDB_info = serviceDB.get_server_info()
            print('connected to: ' + serviceDB_info)

            serviceDB_cursor = serviceDB.cursor()

    except Error as e:
        print("error while connecting: " + e)

    try:
        #select_all_query = "SELECT * FROM serviceqr_testing"
        serviceDB_cursor.execute(query)
        data = serviceDB_cursor.fetchall()
        serviceDB.commit()
        
        if(serviceDB.is_connected()):
            serviceDB_cursor.close()
            serviceDB.close()
            print('connection was closed')
            return data
    except Error as e:
        print("error while reading DB?: ")  
        if(serviceDB.is_connected()):
            serviceDB_cursor.close()
            serviceDB.close()
            print('connection was closed')
        return None

def execute_query(query,data,conf_name,special=False):
    '''
        Func to execute query like UPDATE, ALTER etc.

        Opens connection to the database, performs execution with given query + given data
        Argument special - special way to execute query which is different than the normal way (named poorly ik :* love you)

        Returns:
            If True returns 'True'

            If db connection fails returns 'False'

            If query and execution fails returns 'None'

            If special = True returns last row id
    '''
    try:
        serviceDB = mysql.connector.connect(**service_db_config(conf_name))

        if(serviceDB.is_connected()):
            serviceDB_info = serviceDB.get_server_info()
            print('connected to: ' + serviceDB_info)

            serviceDB_cursor = serviceDB.cursor()

    except Error as e:
        print("error while connecting: " + e)

    try:
        try:
            serviceDB_cursor.execute(query, data)    
            serviceDB.commit()
            if(special):
                last_insert_id = serviceDB_cursor.lastrowid
            print(f"Affected rows: {serviceDB_cursor.rowcount}")
        except Error as e:
            print(f"DB: error: {e}")
            return False
        
        if(serviceDB.is_connected()):
            serviceDB_cursor.close()
            serviceDB.close()
            print('connection was closed')
            if(special):
                return last_insert_id
            return True
    except Error as e:
        print("error while reading DB?: " + e)
        if(serviceDB.is_connected()):
            serviceDB_cursor.close()
            serviceDB.close()
            print('connection was closed')
        return None
        
