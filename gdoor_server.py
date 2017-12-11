import socket
import subprocess

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
    html = """<!DOCTYPE html>
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
        #gdoor_command = "echo 'close' > /home/edge/someFile.txt"
        gdoor_command = "echo CLOSE > /home/edge/someFile.txt"
        doorOpen = False
    else:
        #gdoor_command = "echo 'open' > /home/edge/someFile.txt"
        gdoor_command = "echo OPEN > /home/edge/someFile.txt"
        doorOpen = True
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
    engageDoor()
    response = buildHtml()
    conn.send(response)
    conn.close()
