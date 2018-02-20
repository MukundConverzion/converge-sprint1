import psycopg2
import sys
import pprint

def main():
    conn_string = "host='localhost' dbname='Converge' user='postgres' password='123456789'"
    print ("Connecting to database\n	->%s" % (conn_string))
    # get a connection, if a connect cannot be made an exception will be raised here
     
    # conn.cursor will return a cursor object, you can use this cursor to perform queries
    conn = psycopg2.connect(conn_string)
    cur = conn.cursor()
    cur.execute("CREATE TABLE influencernew (id serial PRIMARY KEY, Name varchar, Profile_Url varchar, Followers varchar, Designation varchar,Link_Url varchar,Postpage_Url varchar,Article_Url varchar);")
    conn.commit()
    print ("Connected!\n")

if __name__ == "__main__":
	main()
    
   
    
    