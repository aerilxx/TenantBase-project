import socketserver
import time

cache = {}

class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
    
        while True:
            if not self.rfile.peek():
                break

            data = self.rfile.readline().strip()
            print("{} wrote: {}".format(self.client_address[0], data))
            data_split = data.split()

            cmdlen = len(data_split)
            command = data_split[0].lower()

            if cmdlen == 6:
                command = data_split[0].lower()

                if command == b"set":                   
                    # set <key> <flags> <exptime> <bytes> <value>
                    key, flags, exptime, length = data_split[1:5]
                    value = data_split[-1]

                    if value:
                        cache[key] = (flags, exptime, length, value)
                        self.wfile.write(b"STORED\r\n")

                    else:
                        print("please provide a value to store. ")

                
            elif cmdlen == 2:
                command = data_split[0].lower()
                key = data_split[1]

                if key not in cache:
                    self.wfile.write(b"you have to initiate the cache first! \r\n")

                else:
                    if command == b"get":
                        
                        if cache[key]:
                            flags, exptime, length, value = cache[key]
                            #output += b"VALUE %s %d %d\r\n%s\r\n" % (key, flags, len(value), value)
                            #print(value)
                            self.wfile.write(value + b" END\r\n")

                            print("value for {k} is {v}".format(k = key, v = value))
                        else:
                            self.wfile.write(b"no value found! \r\n")
                            print("{} is not in cache! ".format(key))

                    elif command == b"delete":
                        key = data_split[1]

                        if cache[key]:
                            del cache[key]
                            print('delete')
                            print(cache)
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
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        server.serve_forever()

