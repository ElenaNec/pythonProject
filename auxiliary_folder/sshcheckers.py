import paramiko

# выполнение команды на удаленной машине и проверка вывода
def ssh_checkout(host, user, passwd, cmd, text, port=22): # user - имя пользователя
    # инициализация клиента, но подключение не выполняем
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # подключение к клиенту
    client.connect(hostname=host, username=user, password=passwd, port=port)
    # выполнение команды и получение результата
    stdin, stdout, stderr = client.exec_command(cmd)
    # сохраняем код возврата
    exit_code = stdout.channel.recv_exit_status()
    out = (stdout.read() + stderr.read()).decode("utf-8")
    # закрываем соединение
    client.close() 
    if text in out and exit_code == 0:
        return True
    else:
        return False


def upload_files(host, user, passwd, local_path, remote_path, port=22):
    print(f"Загружаем файл {local_path} в каталог {remote_path}")
    # объединение транспорта
    transport = paramiko.Transport((host,port))
    # соединение
    transport.connect(None, username=user, password=passwd)
    # создадим объект SFTP
    sftp = paramiko.SFTPClient.from_transport(transport)
    # подключение установлено и все готово, чтобы загружать файл
    # загружаем файл
    sftp.put(local_path, remote_path)
    # проверяем, что подключение создано, и если True то закрываем соединение
    if sftp:
        sftp.close()
    if transport:
        transport.close()


