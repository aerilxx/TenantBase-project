import socketserver
import time
import sqlite3
import sys

cache = {}

def create_db():
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
   
    # check if table exist
    exist = ''' SELECT count(name) FROM sqlite_master WHERE type='table' and name= 'server' '''
    cursor.execute(exist)

    #if the count is 1, then table exists
    if cursor.fetchone()[0]==1:
        pass
    else:
        cursor.execute('''CREATE TABLE server
         (key          TEXT    NOT NULL,
         value          TEXT     NOT NULL)''')

    conn.commit()
    conn.close()

def save_to_db(key,value):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    query = "INSERT INTO server (key,value) VALUES (?,?)"
    data = (key.decode('ascii'), value.decode('ascii'))
    cursor.execute(query, data)

    conn.commit()
    conn.close()

def delete_from_db(key):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    query = "DELETE FROM server where key = ?"
    cursor.execute(query, key.decode('ascii'))
    conn.commit()
    conn.close()

def if_exist(key):
    conn = sqlite3.connect('database.sqlite')
    cursor = conn.cursor()
    query = "SELECT key, value FROM server WHERE key=?"
    data = (key.decode('ascii'))
    cursor.execute(query, data)
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
    
        while True:
            if not self.rfile.peek():
                break
            
            create_db()   
            data = self.rfile.readline().strip()
            print("{} wrote: {}".format(self.client_address[0], data))
            data_split = data.split()

            cmdlen = len(data_split)

            if cmdlen == 6:
                command = data_split[0].lower()

                if command == b"set":                   
                    # set <key> <flags> <exptime> <bytes> <value>
                    key, flags, exptime, length = data_split[1:5]
                    value = data_split[-1]

                    if value:
                        cache[key] = (flags, exptime, length, value)
                        self.wfile.write(b"STORED\r\n")
                        save_to_db(key,value)

                    else:
                        print("please provide a value to store. ")

                
            elif cmdlen == 2:
                command = data_split[0].lower()
                key = data_split[1]

                if key not in cache and not if_exist(key):
                    self.wfile.write(b"you have to initiate the cache first! \r\n")

                else:
                    if command == b"get":
                        
                        if cache[key]:
                            flags, exptime, length, value = cache[key]
                      
                            self.wfile.write(value + b" END\r\n")

                            print("value for {k} is {v}".format(k = key, v = value))
                        else:
                            self.wfile.write(b"no value found! \r\n")
                            print("{} is not in cache! ".format(key))

                    elif command == b"delete":
                        key = data_split[1]

                        if cache[key]:
                            del cache[key]
                            delete_from_db(key)
                            self.wfile.write(b"Delete! \r\n")
                        else:
                            self.wfile.write(b"you cannot delete it because no value found! \r\n")
                            print("You cannot delete {} because it is not saved! ".format(key))

                    else:
                        self.wfile.write(b"please only use get/detele/set commend! \r\n")
            
            else:
                self.wfile.write(b"please check your commend again! \r\n")
    



if __name__ == "__main__":
    HOST, PORT = "127.0.0.1", 11210
    server_address = ("127.0.0.1", 11210)
    print(sys.stderr, 'connecting to %s port %s' % server_address)

    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

