#!/usr/bin/python
import psycopg2

# Within this script a connection with the database is made to retrieve data and print it
# This script could be used to generate a csv file of the database. This could also be achieved by exporting the database to csv with for example: Sequelpro 

def main():
    conn_string = "host='localhost' dbname='dbname' user='username' password='password'"

    # get a connection, if a connect cannot be made an exception will be raised here
    conn = psycopg2.connect(conn_string)

    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    cursor = conn.cursor()

    # variables
    pid_id = []
    pid_title = []
    pid_genre = []
    pid_format = []
    pid_medsyn = []

    # execute our Query
    cursor.execute("SELECT pid FROM bbc_programmes")
    records = cursor.fetchall()
    pid_id = records

    cursor.execute("SELECT pid_title FROM bbc_programmes")
    records = cursor.fetchall()
    pid_title = records

    cursor.execute("SELECT pid_genre FROM bbc_programmes")
    records = cursor.fetchall()
    pid_genre = records

    cursor.execute("SELECT pid_format FROM bbc_programmes")
    records = cursor.fetchall()
    pid_format = records

    cursor.execute("SELECT pid_medsyn FROM bbc_programmes")
    records = cursor.fetchall()
    pid_medsyn = records

    print("pid_id", pid_id)
    print("pid_title", pid_title)
    print("pid_genre", pid_genre)
    print("pid_format", pid_format)
    print("pid_medsyn", pid_medsyn)

if __name__ == "__main__":
    main()



