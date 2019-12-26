import socket
import sys
import _thread
import os
import os.path
from pathlib import Path
import glob
host = "127.0.0.1"
port = int ( sys.argv[1] )
print('Server started..............')
s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)
s.bind((host,port))
s.listen(5)
path01 = 'C:/Users/Admin/Desktop/PA/PA_4/dfs04/'
conf_path = str( path01 + 'dfs.conf.txt' )
def authenticator ( user , passwd ):
    path = Path( conf_path )
    file = open( path , 'r' )
    data = file.read()
    file.close()
    data = data.split('\n')
    n = len(data)
    for i in range(0,n):
        if user in data[i]:
            a = data[i]
            a = a.split(' ')
            print(a)
            if passwd == a[1]:
                return('1')
            else:
                return('0')
        else:
            return('0')
def handler( cs, addr):
    print('New thread created...........')
    m = cs.recv(1024)
    m = m.decode()
    print(m)
    m = m.split('|')
    user = m[0]
    passwd = m[1]
    option = m[2]
    print('User:' + user)
    print('Pass:' + passwd)
    print('Option:' + option)
    x01 = authenticator( user , passwd )
    if ( x01 == '0'):
        print('\nInvalid credentials from DFC..........')
        resp = '0'
        cs.send(resp.encode())
    elif( x01 == '1' ):
        print('\nValid credentials..................')
        resp = '1'
        cs.send(resp.encode())
        
        if option == '1':
            print('PUT option selected...........')
            resp = '1'
            cs.send(resp.encode())
            file_name = cs.recv(1024)
            file_name = file_name.decode()
            print('File_name:' + file_name)
            chunks = cs.recv(1024)
            chunks = chunks.decode()
            ch = chunks.split('|')
            print('Chunks sent are:' + ch[0] + ',' + ch[1])
            z1 = ch[0]
            z2 = ch[1]
            print('Receiving data for chunk:' + z1)
            data = cs.recv( 4096 )
            f = file_name.replace( '.txt' , '')
            f1 = str( file_name + '.' + ch[0])
            f2 = str( file_name + '.' + ch[1])
            cx = str( path01 + 'users/'  + user )
            ch_path = Path( cx)
            if not os.path.isdir( ch_path ):
                os.makedirs( ch_path )
            ch_path1 = Path( str( cx + '/' + f1))
            ch_file = open( ch_path1 , 'wb')
            ch_file.write(data)
            ch_file.close()
            print('data received.')
            print('\n\nReceiving data for chunk:' + z2)
            data = cs.recv( 4096)
            ch_path2 = Path( str( cx + '/' + f2))
            ch_file = open( ch_path2 , 'wb')
            ch_file.write(data)
            ch_file.close()
            print('data received.')
            
            

            
            
            
        elif option == '2':
            print('GET option selected...........')
            resp = '1'
            cs.send(resp.encode())
            file_name = cs.recv(1024)
            file_name = file_name.decode()
            print('File_name:' + file_name)
            chunks = cs.recv(1024)
            chunks = chunks.decode()
            ch = chunks.split('|')
            print('Chunks needed are:' + ch[0] + ',' + ch[1])
            z1 = ch[0]
            z2 = ch[1]
            #print('Receiving data for chunk:' + z1)
            f = file_name.replace( '.txt' , '')
            f1 = str( file_name + '.' + ch[0])
            f2 = str( file_name + '.' + ch[1])
            cx = str( path01 + 'users/'  + user)
            ch_path = Path( cx)
            print('Sending chunk:' + z1)
            ch_path1 = Path( str( cx + '/' + f1))
            ch_path2 = Path( str( cx + '/' + f2))
            if ( os.path.isfile( ch_path1)) and ( os.path.isfile( ch_path2)):
                print('\nRequested chunks present...............')
                resp = '1'
                cs.send(resp.encode())
                ch_file = open( ch_path1 , 'rb')
                data = ch_file.read()
                #cs.send( data )
                ch_file.close()
                print('\nChunk one sent .')
                print('Sending chunk:' + z2)
                ch_file = open( ch_path2 , 'rb')
                data = ch_file.read()
                #cs.send( data )
                ch_file.close()
                print('\nChunk two sent .')
            else:
                print('\nRequested chunk are not present.........')
                resp = '0'
                cs.send(resp.encode())
                
                
            
            

        elif option == '3':
            print('LIST option selected...........')
            list_path1 = 'C:/Users/Admin/Desktop/PA/PA_4/dfs04/users/'
            list_path2 = str( list_path1 + user  )
            list_path3 = str( list_path2 + '/' +'*.txt.*')
            list_path4 = str( list_path2 + '\\' + '\\')
            data = glob.glob(list_path3)
            pathx = Path( list_path2 )
            print('Path one for listing is : ' + list_path2)
            print('Path two for listing is : ' + list_path3)
            print('Path three for listing is : ' + list_path4)
            print('user:' + user)
            n = len(data)
            for i in range(0,n):
                data[i] = data[i].replace( str(list_path2 + '\\') , '')
            data_s = data[0]
            for i in range(1,n):
                data_s += str('|' + data[i])
            print('Message to DFC is: ' + data_s)
            
                
            print('The chunks in DFS04 are:')
            print(data)
            
            listx = data_s
            cs.send(listx.encode())

        else:
            print('Invalid option................')
            resp = '0'
            cs.send(resp.encode())
        
            
        
while True:
    try:
        (cs,addr) = s.accept()
        #s.connect(cs)
        print('Connection accepted..........')
        _thread.start_new_thread(handler, (cs,addr))


    except KeyboardInterrupt:
        sys.exit()

    except:
        pass
