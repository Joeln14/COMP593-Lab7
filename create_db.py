"""
Description:
 Creates the people table in the Social Network database
 and populates it with 200 fake people.

Usage:
 python create_db.py
"""
import os
import inspect
import sqlite3
from faker import Faker
from datetime import datetime 
import re

def main():
    global db_path
    db_path = os.path.join(get_script_dir(), 'social_network.db')
    create_people_table()
    populate_people_table()

def create_people_table():
    """Creates the people table in the database"""
    
    con = sqlite3.connect('social_network.db')
    cur = con.cursor() 

    create_ppl_tbl_query = """
        CREATE TABLE IF NOT EXISTS people
        (

            id          INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            email       TEXT NOT NULL,
            address     TEXT NOT NULL,
            city        TEXT NOT NULL,
            province    TEXT NOT NULL,
            bio         TEXT,
            age         INTEGER,
            created_at  DATETIME NOT NULL,
            updated_at  DATETIME NOT NULL

        );
    """

    cur.execute(create_ppl_tbl_query)
    con.commit()
    con.close

    return

def populate_people_table():
    """Populates the people table with 200 fake people"""
    con = sqlite3.connect(db_path)
    cur = con.cursor()

    add_person_query = """
        INSERT INTO people
        (
            name,
            email,
            address,
            city,
            province,
            bio,
            age,
            created_at,
            updated_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    fake = Faker("en_CA")
    fake_us = Faker("en_US")
    num_people = 200 
    

    for p in range(num_people):

        regex = '(.*?)\s(.*)'
        
        name = fake.name()

        match = re.match(regex, name)

        new_person =   (name,
                        f'{match.group(1)}.{match.group(2)}@{fake.domain_name()}',
                        fake.address(),
                        fake.city(),
                        fake.province(),
                        fake_us.sentence(nb_words=10),
                        fake.random_int(min=1, max=100),
                        datetime.now(),
                        datetime.now())
        
        cur.execute(add_person_query, new_person)

    con.commit()
    con.close()


    return

def get_script_dir():
    """Determines the path of the directory in which this script resides

    Returns:
        str: Full path of the directory in which this script resides
    """
    script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
    return os.path.dirname(script_path)

if __name__ == '__main__':
   main()