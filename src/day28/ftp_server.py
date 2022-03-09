from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from pyftpdlib.handlers import FTPHandler

# 启动ftp 服务器 控制对文件的访问
# python 指令开启服务端 python -m pyftpdlib -i 127.0.0.1 -w -d /file/ -u user -P 123456
if __name__ == '__main__':
    authorizer = DummyAuthorizer()
    '''
        权限说明：
        Read permissions:
         - "e" = change directory (CWD command)
         - "l" = list files (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
         - "r" = retrieve file from the server (RETR command)

        Write permissions:
         - "a" = append data to an existing file (APPE command)
         - "d" = delete file or directory (DELE, RMD commands)
         - "f" = rename file or directory (RNFR, RNTO commands)
         - "m" = create directory (MKD command)
         - "w" = store a file to the server (STOR, STOU commands)
         - "M" = change file mode (SITE CHMOD command)
         - "T" = update file last modified time (MFMT command)
    '''
    # 管理员账号
    authorizer.add_user('admin', 'admin', 'E:\\py\\day27', perm='elradfmwMT')
    # 普通账号 默认只有浏览权限
    authorizer.add_user('user', 'user', 'E:\\py\\day27')
    handler = FTPHandler
    handler.authorizer = authorizer
    ftp_server = FTPServer(('0.0.0.0', 8888), handler)
    # 启动ftp 服务器
    ftp_server.serve_forever()
