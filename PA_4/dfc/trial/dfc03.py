import os
import sys
import socket
import time
import base64
import os.path
import hashlib
import cryptography
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
cred = []
path01 = 'C:/Users/Admin/Desktop/PA/PA_4/dfc/'
#path02 = path01
path02 = 'C:/Users/Admin/Desktop/PA/test/'
path_ch = str( path02 + 'chunks/')
dfs_ports = []
access_right = 0o777
host = "127.0.0.1"
end = 'x'
data_list = []

def reader ( pathz , key ):
    print('\n\n\n Entering reader..............')
    file = open ( pathz , 'rb')
    file_data = file.read
    file.close()
    print('$$$$$$$')
    print('Decrypting the file inside reader.................')
    en_data01 = key.decrypt( file_data )
    print('Decoding the file..............................')
    en_data02 = en_data01.decode()
    data_list.append(en_data02)
    print('Decrypted and decoded data:' )
    print(en_data02)
    print('returning...............')
    return
    
          
    
    
    

def decrypt( file_name , user , key ):
    fil = file_name.replace('.txt' , '')
    c1 = str( file_name + '.1')
    c2 = str( file_name + '.2')
    c3 = str( file_name + '.3')
    c4 = str( file_name + '.4')
    
    p1 = str( path02 + 'chunks/' + fil + '/')
    p2 = str( path01 + 'users/' + user + '/Complete_files/' )
    cp1 = Path (str( p1 + c1 ))
    cp2 = Path(str( p1 + c2 ))
    cp3 = Path(str( p1 + c3 ))
    cp4 = Path(str( p1 + c4 ))

    if( os.path.isfile( cp1) and os.path.isfile( cp2) and os.path.isfile( cp3) and os.path.isfile( cp4)):
        print('File complete..............')
        print('Reconstructing the file...............')
        print('Decrypting first chunk..............')
        pa1 = Path( str(p1 + c1))
        pa2 = Path( str(p1 + c2))
        pa3 = Path( str(p1 + c3))
        pa4 = Path( str(p1 + c4))
        x10 = reader( pa1 , key )
        x10 = reader( pa2 , key )
        x10 = reader( pa3 , key )
        x10 = reader( pa4 , key )
        
        
        return
        
    
    
def rec(file_name , c1 , c2, port):
    user = cred[0]
    passwd = cred[1]
    print('\nUser_name:' + user )
    print('\npassword:' + passwd)
    print('\nport:' + str(port))
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    msg = str( user_name + '|' + passwd + '|' + '2')
    f = file_name.encode()
    try:
        s.connect((host,port))
        print('Success')
        s.send(msg.encode())
        resp = s.recv(1024)
        resp = str( resp.decode())
        print('response:' + resp)
        if resp == '1':
            print('\nServer has authenticated the input..........Proceed')
            resp = s.recv(1024)
            resp = str( resp.decode())
            if resp == '0':
                print('Invalid option........')
            else:
                print('Valid option.............')
                s.send(f)
                chunks = str(c1 + '|' + c2)
                s.send(chunks.encode())
                resp = s.recv(1024)
                resp = resp.decode()
                if resp == '2':
                    try:
                        chu01 = s.recv(4096)
                        print('#########')
                    except:
                        dum = 'xxx'
                        chu01 = dum.encode()
                    try:
                        chu02 = s.recv(4096)
                    except:
                        print('########')
                        dum = 'xxx'
                        chu02 = dum.encode()
                    s.close()
                    if ( chu01 and chu02 ):
                        print('GET operation success................')
                        fil = file_name.replace( '.txt' , '')
                        path_rec = str( path01 + 'users/' + user +  '/' + 'chunks/' + fil  )
                        print(path_rec)
                        dir_path = Path( path_rec)
                        #file = file_name.replace
                        print('xxxxxxxxxxx')
                        if not os.path.isdir(dir_path):
                            os.makedirs( dir_path , access_right )
                            print('xxxxxxxxxxxxxxxx')
                        fil1 = str( file_name + '.' + c1)
                        fil2 = str( file_name + '.' + c2)
                        c_path1 = Path( str( path_rec + '/' + fil1))
                        c_path2 = Path( str( path_rec + '/' + fil2))
                        file = open( c_path1 , 'wb')
                        file.write( chu01 )
                        file.close()
                        file = open( c_path2 , 'wb')
                        file.write( chu02 )
                        file.close()
                        
                
                        
                
                    
                    
                                    
                    
                elif resp == '0':
                    print('\n\nFile not found in the server.............................')
                    return

                else:
                    print('Alright')
                    print('GET operation success................')
                    chu01 = end.encode()
                    chu02 = end.encode()
                    fil = file_name.replace( '.txt' , '')
                    path_rec = str( path01 + 'users/' + user +  '/' + 'chunks/' + fil  )
                    print(path_rec)
                    dir_path = Path( path_rec)
                    #file = file_name.replace
                    print('xxxxxxxxxxx')
                    if not os.path.isdir(dir_path):
                        os.makedirs( dir_path , access_right )
                        print('xxxxxxxxxxxxxxxx')
                    fil1 = str( file_name + '.' + c1)
                    fil2 = str( file_name + '.' + c2)
                    c_path1 = Path( str( path_rec + '/' + fil1))
                    c_path2 = Path( str( path_rec + '/' + fil2))
                    file = open( c_path1 , 'wb')
                    file.write( chu01 )
                    file.close()
                    file = open( c_path2 , 'wb')
                    file.write( chu02 )
                    file.close()
                
                    s.close()
                    return


        else:
            print('\nInvalid input to the server................')
            s.close()
            return

    except:
        print('error')
        return

                
    
def sender( file_name , c1 , c2, port):
    user = cred[0]
    passwd = cred[1]
    print('\nUser_name:' + user )
    print('\npassword:' + passwd)
    print('\nport:' + str(port))
    s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
    msg = str( user_name + '|' + passwd + '|' + '1')
    f = file_name.encode()
    try:
        s.connect((host,port))
        print('Success')
        s.send(msg.encode())
        resp = s.recv(1024)
        resp = str( resp.decode())
        print('response:' + resp)
        if resp == '1':
            print('\nServer has authenticated the input..........Proceed')
            resp = s.recv(1024)
            resp = str( resp.decode())
            if resp == '0':
                print('Invalid option........')
            else:
                print('Valid option.............')
                s.send(f)
                chunks = str(c1 + '|' + c2)
                s.send(chunks.encode())
                f = file_name.replace('.txt' , '')
                ck1 = str( file_name + '.' + c1)
                ck2 = str( file_name + '.' + c2)
                path_x1 = Path (str( path_ch + '/' + f + '/' + ck1))
                path_x2 = Path (str( path_ch + '/' + f + '/' + ck2))
                ch01 = open(path_x1 , 'rb')
                data = ch01.read()
                ch01.close()
                s.send(data)
                ch02 = open(path_x2 , 'rb')
                data = ch02.read()
                ch02.close()
                s.send( data )
                s.close()
                return
        else:
            print('\nInvalid input to the server................')
            s.close()
            return

    except:
        print('error')
        return



    
   

def key_maker(passwd):
    salt01 = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt = salt01,
        iterations = 100000,
        backend = default_backend(),
        )
    p1 = passwd.encode()
    key = base64.urlsafe_b64encode(kdf.derive(p1))
    f = Fernet(key)
    return(f)

def splicer( v , l , file_name , passwd ):
    print('\n\n Entering splicer..............................')
    fol= file_name.replace('.txt' , '')
    r = len(l)
    chunk_data = ' '
    chunk_n = file_name + '.'+ v
    temp =  str( path02 + 'chunks/' + fol)
    temp_path = Path( temp )
    if not ( os.path.isdir( temp_path )):
        os.makedirs( temp_path , access_right )
    chunk_path = Path( str( temp + '/' + chunk_n))
    for i in range(0,r):
        chunk_data += l[i]
    print('\n\nData for this chunk:' + chunk_data)
    print('\nEncrypting the chunk................................')
    en_key = key_maker( passwd )
    if en_key:
        print('\nEncryption key created successfully....................')
        en_data = en_key.encrypt( chunk_data.encode() )
    else:
        print('\nEncryption key failure, Encryption failed......................')
        en_data = chunk_data.encode()
    chunk_file = open( chunk_path , 'wb')
    chunk_file.write( en_data)
    return


def hasher( file_path ):
    print('\n\n Inside Hasher....................')
    file = open( file_path , 'rb')
    file_data = file.read()
    h01 = hashlib.md5( file_data )
    h02 = h01.hexdigest()
    h03 = int( h02 , 16)
    mod4 = str( h03 % 4)
    return( mod4)

def get( user_name , passwd ):
    print('\n Entering get function.........................')
    print('\n Please enter the file_name to get the pieces...................')
    file_name = str (input('\n\n=>'))
    pat = file_name.replace('.txt' , '_pattern.txt')
    file_pat_path = Path( str( path01 + 'pattern/' + pat))
    if not os.path.isfile( file_pat_path ):
        print('\n Invalid file requested from the DFS..................')
        return('0')
    else:
        pat_file = open( file_pat_path , 'r')
        val_pat = str (pat_file.read())
        x03 = val_pat
        pat_file.close()
        print('Pattern for:' +' ' + file_name + 'is:' + val_pat)
        c1 = int(dfs_ports[0])
        c2 = int(dfs_ports[1])
        c3 = int(dfs_ports[2])
        c4 = int(dfs_ports[3])
        if x03 == '0':
            print('\n\n Pattern 0 selected, \n(1,2) => dfs01 \n(2,3) => dfs02 \n(3,4) => dfs03 \n(4,1) => dfs04')
            
            x05 = rec(  file_name , '1' , '2' , c1)
            x05 = rec(  file_name , '2' , '3' , c2)
            x05 = rec(  file_name , '3' , '4' , c3)
            x05 = rec(  file_name , '4' , '1' , c4)

        if x03 == '1':
            print('\n\n Pattern 1 selected, \n(1,2) => dfs02 \n(2,3) => dfs03 \n(3,4) => dfs04 \n(4,1) => dfs01')
           
            x05 = rec(  file_name , '4' , '1' , c1)
            x05 = rec(  file_name , '1' , '2' , c2)
            x05 = rec(  file_name , '2' , '3' , c3)
            x05 = rec(  file_name , '3' , '4' , c4)

        if x03 == '2':
            print('\n\n Pattern 2 selected, \n(1,2) => dfs03 \n(2,3) => dfs04 \n(3,4) => dfs01 \n(4,1) => dfs02')
            
            x05 = rec(  file_name , '3' , '4' , c1)
            x05 = rec(  file_name , '4' , '1' , c2)
            x05 = rec(  file_name , '1' , '2' , c3)
            x05 = rec(  file_name , '2' , '3' , c4)

        if x03 == '3':
            print('\n\n Pattern 3 selected, \n(1,2) => dfs04 \n(2,3) => dfs01 \n(3,4) => dfs02 \n(4,1) => dfs03')
            
            x05 = rec(  file_name , '2' , '3' , c1)
            x05 = rec(  file_name , '3' , '4' , c2)
            x05 = rec(  file_name , '4' , '1' , c3)
            x05 = rec(  file_name , '1' , '2' , c4)

        print('\n\nReconstructing the file from the chunks received...........................')
        fil = file_name.replace( '.txt' , '')
        path_rec = str( path01 + 'users/' + user_name +  '/' + 'chunks/' + fil  )
        print(path_rec)
        dir_path = Path( path_rec)
        fil1 = str( file_name + '.1')
        fil2 = str( file_name + '.2')
        fil3 = str( file_name + '.3')
        fil4 = str( file_name + '.4')
        c_path1 = Path( str( path_rec + '/' + fil1))
        c_path2 = Path( str( path_rec + '/' + fil2))
        c_path3 = Path( str( path_rec + '/' + fil3))
        c_path4 = Path( str( path_rec + '/' + fil4))
        if not ( os.path.isfile( c_path1) and os.path.isfile( c_path2) and os.path.isfile( c_path3) and os.path.isfile( c_path4)):
            print('\nSome of the chunks are not found................')
            print('\n' + file_name + ' : Incomplete\n\n\n\n\n.................................................\n\n\n\n')
            return('1')

        else:
            print('\nAll the four chunks for the file is present, preparing for reconstruction.................')
            print('\nAttempting to decrypt the chunks...................')
            print('\nPlease enter your password to decrypt the file:')
            pa = str (input('\n\n=>'))
            while ( pa != passwd):
                print('\nPassword incorrect............  please enter right password...........')
                pa = str (input('\n\n=>'))
               
            print('\n\nDecrypting the chunks with the password..............')
            key = key_maker(passwd)
            x06 = decrypt( file_name , user_name , key )
            print('Complete data:')
            print( data_list )
            
            return('1')
            
            #x06 = recon( file_name )

        return('1')
    
def put( user_name , passwd ):
    print('\n Entering put function..........................')
    print('\n Please enter the file_name to perform splitting..............')
    file_name = str( input('\n\n=>'))
    file_path = Path( str( path01 + file_name))
    if not os.path.isfile(file_path):
        print('\n The file specified, does not exist.....................')
        return('0')
    else:
        print('\n The file: ' + file_name + ' exists')
        print('\n Performing hashing to determine the order for recipient dfs.................')
        x03 = hasher( file_path )
        pat = file_name.replace('.txt' , '_pattern.txt')
        file_pat_path = Path( str( path01 + 'pattern/' + pat))
        file_pat = open( file_pat_path , 'w')
        file_pat.write( x03 )
        file_pat.close()
        file = open( file_path , 'r')
        file_data = file.read()
        file.close()
        l = []
        for i in file_data:
            l.append(i)
        n = len(l)
        mod = int( n%4)
        n2 = int(n - mod)
        v1 = int(n2/4)
        v2 = int(n2/2)
        v3 = int(v1*3)
        a = l[0:v1]
        b = l[v1:v2]
        c = l[v2:v3]
        d = l[v3:n]
        print('\n\n\nCreating first chunk.....................')
        print(a)
        x04 = splicer( '1' , a , file_name , passwd)
        print('\n\nCreating second chunk......................')
        print(b)
        x04 = splicer( '2' , b , file_name , passwd)
        print('\n\nCreating third chunk........................')
        print(c)
        x04 = splicer('3' , c , file_name , passwd)
        print('\n\nCreating fourth chunk......................')
        print(d)
        x04 = splicer('4' , d , file_name , passwd)

        print('\n\nSending the chunks to the DFS....................')
        c1 = int(dfs_ports[0])
        c2 = int(dfs_ports[1])
        c3 = int(dfs_ports[2])
        c4 = int(dfs_ports[3])
        if x03 == '0':
            print('\n\n Pattern 0 selected, \n(1,2) => dfs01 \n(2,3) => dfs02 \n(3,4) => dfs03 \n(4,1) => dfs04')
            
            x05 = sender(  file_name , '1' , '2' , c1)
            x05 = sender(  file_name , '2' , '3' , c2)
            x05 = sender(  file_name , '3' , '4' , c3)
            x05 = sender(  file_name , '4' , '1' , c4)

        if x03 == '1':
            print('\n\n Pattern 1 selected, \n(1,2) => dfs02 \n(2,3) => dfs03 \n(3,4) => dfs04 \n(4,1) => dfs01')
           
            x05 = sender(  file_name , '4' , '1' , c1)
            x05 = sender(  file_name , '1' , '2' , c2)
            x05 = sender(  file_name , '2' , '3' , c3)
            x05 = sender(  file_name , '3' , '4' , c4)

        if x03 == '2':
            print('\n\n Pattern 2 selected, \n(1,2) => dfs03 \n(2,3) => dfs04 \n(3,4) => dfs01 \n(4,1) => dfs02')
            
            x05 = sender(  file_name , '3' , '4' , c1)
            x05 = sender(  file_name , '4' , '1' , c2)
            x05 = sender(  file_name , '1' , '2' , c3)
            x05 = sender(  file_name , '2' , '3' , c4)

        if x03 == '3':
            print('\n\n Pattern 3 selected, \n(1,2) => dfs04 \n(2,3) => dfs01 \n(3,4) => dfs02 \n(4,1) => dfs03')
            
            x05 = sender(  file_name , '2' , '3' , c1)
            x05 = sender(  file_name , '3' , '4' , c2)
            x05 = sender(  file_name , '4' , '1' , c3)
            x05 = sender(  file_name , '1' , '2' , c4)
        return('1')
        
def authenticator(  ):
    print('\nReading dfc.conf file................................')
    conf_path = Path( str( path01 + 'dfc.conf.txt') )
    conf_file = open( conf_path , 'r' )
    conf_data = conf_file.read()
    d1 = conf_data.split('\n')
    dfs_ports.clear()
    for i in range(0,4):
        dfs_ports.append(d1[i][22::])
    print('\n\nThe ports for the DFS are:')
    print(dfs_ports)
    cred.clear()
    for i in range(4,5):
        cred.append(d1[i][10::])
        cred.append(d1[i+1][10::])
    return('1')
    



print('Welcome to the Distributed File system project........................')
print('\n DFC...................')
while True:
    x01 = authenticator()
    #user_name = credentials[0]
    #passwd = credentials[1]
    if x01 =='0':
        print( '\n User credentials are invalid..................')
    else:
        print('\n.............................................................\n...........................................................................................................................................\n\n')
        print(cred)
        user_name = cred[0]
        passwd = cred[1]
        print( 'User:' + user_name)
        print('Pass:' + passwd )
        print('\n Please select any one of the following options.....................')
        print('\n [1] for PUT \n [2] for GET \n [3] for LIST \n [0] for EXIT........................')
        option = str(input('\n\n=>'))
        if option == '0':
            print('\n You have selected to exit DFC.......................\n\n Exiting DFC')
            sys.exit(0)
            
        elif option == '1':
            print('\nPUT operation selected..........................')
            x02 = put( user_name , passwd )
            
            if x02 == '0':
                print('\n PUT operation failed............')
                print('\n Try again.................')
            else:
                print('\n\n PUT operation successful.........................')
                print('\n\n\n.......................................................................................................................................................\n.................................................................................................................................................\n...............................................................................................................................................')
                

        elif option == '2':
            print('\nGET operation selected..........................')
            x02 = get( user_name , passwd )

            if x02 == '0':
                print('\n GET operation failed..................')
                print('\n Try again...............')
            else:
                print('\n\n GET operation successful.........................')
                print('\n\n\n.......................................................................................................................................................\n.................................................................................................................................................\n...............................................................................................................................................')
                

                
                

        elif option == '3':
            print('\nLIST operation selected.........................')

        else:
            print('\nInvalid option.......................................Try again...............')
            
        

        
    
