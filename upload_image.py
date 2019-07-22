import paramiko
import platform

def upload(hostname,username,password,image):
    ssh_client =paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=hostname,username=username, password=password)

    ftp_client=ssh_client.open_sftp()
    #ftp_client.put('test_images/reading.jpg','/var/www/html/images/reading.jpg')
    if platform.system() == 'Windows':
        imageFileName = image.split('\\')[-1]
    else:
        imageFileName = image.split('/')[-1]

    ftp_client.put(image,imageFileName)

    ftp_client.close()
    stdin, stdout, stderr = ssh_client.exec_command('sudo rm /var/www/html/images/*')
    stdin.write('Hilyw131567_\n')
    ssh_client.exec_command('sudo mv '+imageFileName+' /var/www/html/images/'+imageFileName)
    #print(stdout.readlines())
    ssh_client.close()

