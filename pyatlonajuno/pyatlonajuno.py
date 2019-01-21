import time
import socket

import telnetlib


class Juno451Exception(Exception):
    pass


class Juno451ConnectionFailureException(Juno451Exception):
    pass


class Juno451BadServerException(Juno451Exception):
    pass


class Juno451InvalidUsernameException(Juno451Exception):
    pass


class Juno451InvalidPasswordException(Juno451Exception):
    pass


class Juno451IllegalArgumentException(Juno451Exception):
    pass

class Juno451:
    def __init__(self, username, password, host, port=23, debug=False, timeout=5):
       self.username = username
       self.password = password
       self.host = host
       self.port = port
       self.debug = debug
       self.timeout = timeout #seconds
       self.conn = telnetlib.Telnet()

    def login(self):
        conn = self.conn
        if self.debug:
            conn.set_debuglevel(10)
        try:
            conn.open(self.host, self.port, self.timeout)
        except socket.timeout as e:
            raise Juno451ConnectionFailureException(
                "Could not connect to {host}:{port}. {message}. Is telnet enabled on the Juno 451?"
                .format(host=self.host, port=self.port, message=e))
        prompt = conn.read_until("Username :", self.timeout)
        if "Login Please" not in prompt:
            raise Juno451BadServerException(
                "'Login Please' prompt not recieved, is the telnet server deinitely an Atlona Juno 451?"
                " Received: {prompt}".format(prompt=prompt)
            )
        conn.write((self.username+'\r\n').encode('ascii'))
        if "Password" not in conn.read_until("Password :", self.timeout):
            raise Juno451InvalidUsernameException(
                "Could not complete login process, user: {user} is not valid"
                .format(user=self.username)
            )
        conn.write((self.password+'\r\n').encode('ascii'))
        if "Welcome to TELNET" not in conn.read_until("Welcome to TELNET.", self.timeout):
            raise Juno451InvalidPasswordException(
                "Could not complete login process, password is invalid."
                .format(user=self.username)
            )
        # Without this sleep, when command() runs read_until it receives "Welcome to TELNET." again.
        time.sleep(1)

    def command(self, command):
        self.login()
        self.conn.write(command+"\r\n")
        self.conn.read_until("\n", self.timeout)
        result = self.conn.read_until("\n", self.timeout)
        self.conn.close()
        return result.strip()

    def getPowerState(self):
        """returns on or off"""
        return self.command("PWSTA").lower().lstrip("pw")

    def setPowerState(self, state):
        if state =="on":
            return self.command("PWON")
        elif state =="off":
            return self.command("PWOFF")
        else:
            raise Juno451IllegalArgumentException(
                "Invalid power state: {state}, should be on or off."
                .format(state=state))

    def getInputState(self):
        """Returns array of booleans, one for each input, True=connected"""
        return [i == "1" for i in self.command("InputStatus").lstrip("InputStatus ")]

    def getSource(self):
        result = self.command("Status")
        return int(result[1])

    def setSource(self, source):
        if int(source) not in range(1,5):
            raise Juno451IllegalArgumentException(
                "Source: {source} not valid, must be 1,2,3 or 4"
                .format(source=source))
        return self.command("x{source}AVx1".format(source=source))[1]
