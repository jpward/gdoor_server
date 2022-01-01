import socket
import subprocess
import time

def getRedirect(redirect):
    if redirect:
        return """<meta http-equiv="refresh" content="3; URL=http://192.168.1.121" />"""
    else:
        return """ """

def getDoorState():
    gdoor_open_cmd = ['cat', '/sys/class/gpio/gpio49/value']
    gdoor_opened = subprocess.check_output(gdoor_open_cmd)
    gdoor_close_cmd = ['cat', '/sys/class/gpio/gpio115/value']
    gdoor_closed = subprocess.check_output(gdoor_close_cmd)
    if gdoor_opened == "1\n":
        print("door is open")
        return """value="Close Garage Door" """
    elif gdoor_closed == "1\n":
        print("door is closed")
        return """value="Open Garage Door" """
    else:
        print("door is moving")
        return """value="Stop Garage Door" """

def buildHtml(redirect):
    #HTML to send to browsers
    html = """HTTP/1.1 200 OK
Connection: close\r\n\r\n
<!DOCTYPE html>
<html>
<head> <title>Garage Options</title> """ + getRedirect(redirect) + """ </head>
<center><h2>Garage</h2></center>
<form method='GET' action='/toggle'>
  <input type="submit" """ + getDoorState() + """>
  <input type="checkbox" id="override" name="override" value="yes">
    <label for="override"> Override</label><br>
</form>
</html>
"""
    return html

def engageDoor(override):
    gdoor_open_cmd = ['cat', '/sys/class/gpio/gpio49/value']
    gdoor_opened = subprocess.check_output(gdoor_open_cmd)

    gdoor_close_cmd = ['cat', '/sys/class/gpio/gpio115/value']
    gdoor_closed = subprocess.check_output(gdoor_close_cmd)

    print("engage door %s %s" % (gdoor_opened, gdoor_closed) )

    if gdoor_opened == "1\n" or gdoor_closed == "1\n" or override:
        gdoor_command = ""
        
        print("simulating button down")
        gdoor_command = "echo 1 > /sys/class/gpio/gpio48/value"
        process = subprocess.call( gdoor_command, shell=True )

        max_sleep_cnt = 0
        while gdoor_opened != "0\n" or gdoor_closed != "0\n":
            if max_sleep_cnt > 20:
                break
            time.sleep(0.2)
            max_sleep_cnt = max_sleep_cnt + 1
            gdoor_opened = subprocess.check_output(gdoor_open_cmd)
            gdoor_closed = subprocess.check_output(gdoor_close_cmd)

        print("simulating button up")
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
    redirect = False
    if str(request).find("GET /toggle") > -1:
        override = str(request).find("override=yes") > -1
        engageDoor(override)
        redirect = True

    response = buildHtml(redirect)
    conn.send(response)
    conn.close()
