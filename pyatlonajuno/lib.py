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


def ea(s):
    """ Encode Ascii """
    return s.encode('ascii')


def da(b):
    """ Decode Ascii """
    try:
        return b.decode('ascii')
    except Exception:
        return b


class Juno451:
    def __init__(self, username, password, host,
                 port=23, debug=False, timeout=5):
        self.username = username
        self.password = password
        self.host = host
        self.port = int(port)
        self.debug = debug
        self.timeout = int(timeout)  # seconds
        self.conn = telnetlib.Telnet()

    def login(self):
        conn = self.conn
        if self.debug:
            conn.set_debuglevel(10)
        try:
            conn.open(self.host, self.port, self.timeout)
        except socket.timeout as e:
            raise Juno451ConnectionFailureException(
                "Could not connect to {host}:{port}. {message}."
                " Is telnet enabled on the Juno 451?"
                .format(host=self.host, port=self.port, message=e))
        prompt = da(conn.read_until(ea("Username :"), self.timeout))
        if "Login Please" not in prompt:
            raise Juno451BadServerException(
                "'Login Please' prompt not recieved, is the"
                " telnet server definitely an Atlona Juno 451?"
                " Received: {prompt}".format(prompt=prompt)
            )
        conn.write((self.username+'\r\n').encode('ascii'))
        if "Password" not in da(conn.read_until(ea("Password :"),
                                                self.timeout)):
            raise Juno451InvalidUsernameException(
                "Could not complete login process, user: {user} is not valid"
                .format(user=self.username)
            )
        conn.write((self.password+'\r\n').encode('ascii'))
        response = da(conn.read_until(ea("Welcome to TELNET."), self.timeout))
        if "Welcome to TELNET" not in response:
            raise Juno451InvalidPasswordException(
                "Could not complete login process, password is invalid."
                .format(user=self.username)
            )
        # Without this sleep, when command() runs read_until
        # it receives "Welcome to TELNET." again.
        time.sleep(1)

    def command(self, command):
        self.login()
        self.conn.write(ea(command+"\r\n"))
        self.conn.read_until(ea("\n"), self.timeout)
        result = da(self.conn.read_until(ea("\n"), self.timeout))
        self.conn.close()
        return result.strip()

    def getPowerState(self):
        """returns on or off"""
        return self.command("PWSTA").lower().lstrip("pw")

    def setPowerState(self, state):
        if state == "on":
            return self.command("PWON")
        elif state == "off":
            return self.command("PWOFF")
        else:
            raise Juno451IllegalArgumentException(
                "Invalid power state: {state}, should be on or off."
                .format(state=state))

    def getInputState(self):
        """Returns booleans per input, True=connected"""
        return [i == "1" for i in
                self.command("InputStatus").lstrip("InputStatus ")]

    def getSource(self):
        result = self.command("Status")
        return int(result[1])

    def setSource(self, source):
        if int(source) not in range(1, 5):
            raise Juno451IllegalArgumentException(
                "Source: {source} not valid, must be 1,2,3 or 4"
                .format(source=source))
        return int(self.command("x{source}AVx1".format(source=source))[1])
