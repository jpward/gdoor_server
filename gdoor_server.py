import socket
import subprocess
import time

doorOpen = True
def getDoorState():
    if doorOpen:
        print("door is open")
        return """value="Close Garage Door" """
    else:
        print("door is closed")
        return """value="Open Garage Door" """


def buildHtml():
    #HTML to send to browsers
    html = """HTTP/1.1 200 OK
Connection: close\r\n\r\n
<!DOCTYPE html>
<html>
<head> <title>Garage Options</title> </head>
<center><h2>Garage</h2></center>
<form method='GET' action='/toggle'>
  <input type="submit" """ + getDoorState() + """>
</form>
</html>
"""
    return html

def engageDoor():
    global doorOpen
    gdoor_command = ""
    if doorOpen:
        doorOpen = False
    else:
        doorOpen = True

    gdoor_command = "echo 1 > /sys/class/gpio/gpio48/value"
    process = subprocess.call( gdoor_command, shell=True )

    time.sleep(4)
    gdoor_command = "echo 0 > /sys/class/gpio/gpio48/value"
    process = subprocess.call( gdoor_command, shell=True )

#Setup Socket WebServer
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)
while True:
    conn, addr = s.accept()
    print("Got a connection from %s" % str(addr))
    request = conn.recv(1024)
    print("Content = %s" % str(request))
    #request = str(request)
    if str(request).find("GET /toggle") > -1:
        engageDoor()

    response = buildHtml()
    conn.send(response)
    conn.close()
