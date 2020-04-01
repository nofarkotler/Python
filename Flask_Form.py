import paramiko
from flask import Flask, render_template, request  # Import the Flask class

app = Flask(__name__)  # create an instance of this class

@app.route("/")  # tell Flask what URL should trigger our function
def Html_Form():
    return render_template('html1.htm')  # run the Html Form

# the paramiko connection
@app.route("/", methods=['POST'])
def Remote_connect():
    x = request.form['name1']
    y = request.form['name2']
    print("please wait, creating ssh client...")
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # avoid the assurance question before connecting
    print("please wait, connecting with remote server... ")
    ssh_client.connect(hostname='192.168.8.103', username='root', password='123456')  # uses port 22
    cmd = "cd /root/Flask; python script.py;"
    print("please wait executing command on remote server...")
    stdin, stdout, stderr = ssh_client.exec_command(cmd)
    stdin.write(x + '\n')
    stdin.write(y + '\n')
    stdin.flush()
    print("Succesfully executed command on remote server")
    stdout = stdout.readlines()
    stdout = "".join(stdout)  # more readable
    return render_template('handler.htm', text=stdout)
    ssh_client.close()


if __name__ == "__main__":  # This will run the application.This will help us trace the errors.
    app.run(debug=True)


