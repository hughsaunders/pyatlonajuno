import requests

# x${input}AVx1
# curl -v "http://hdmi/aj.html?a=command&cmd=x1AVx1"
# curl -v "http://hdmi/aj.html?a=command&cmd=PWON"

# curl -va "http://hdmi/aj.html?a=avs"
# {"login_ur":1,"inp":1,"asw":0,"HDMIAud":1,"ARC":0,"Toslink":1,"HDCPSet":[1,1,1,1]}

# curl -va "http://hdmi/aj.html?a=sys"
# {"login_ur":1,"tp":23,"tel_log":1,"ttimeout":120,"broad":1,"PW":1,"Lock_obj":0}


class Juno451IllegalArgumentException(Exception):
    pass


class Juno451:
    def __init__(self, url, debug=False, timeout=5):
        self.requests = requests
        self.url = url
        self.debug = debug
        self.timeout = int(timeout)  # seconds

    def getPowerState(self):
        """returns on or off"""
        if self.requests.get(self.url+"/aj.html?a=sys").json()['PW'] == 1:
            return "on"
        else:
            return "off"

    def setPowerState(self, state):
        if state == "on":
            self.requests.get(self.url+"/aj.html?a=command&cmd=PWON")
        elif state == "off":
            self.requests.get(self.url+"/aj.html?a=command&cmd=PWOFF")
        else:
            raise Juno451IllegalArgumentException(
                "Invalid power state: {state}, should be on or off."
                .format(state=state))

    def getSource(self):
        return self.requests.get(self.url+"/aj.html?a=avs").json()['inp']

    def setSource(self, source):
        if int(source) not in range(1, 5):
            raise Juno451IllegalArgumentException(
                "Source: {source} not valid, must be 1,2,3 or 4"
                .format(source=source))
        self.requests.get(
            self.url+"/aj.html?a=command&cmd=x{}AVx1".format(source))
