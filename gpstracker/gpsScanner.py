import math
import threading
from gps import *
from datetime import datetime
import logging
logger = logging.getLogger(__name__)


class GPSScanner():
    locationHash = None
    runLocationThread = None
    gpsd = None

    # The locationHash is only valid if at least one TPV and one SKY message has been received
    TPV_message_received = False
    SKY_message_received = False

    def __init__(self):
        pass

    def runLocate(self):
        logger.debug('Starting location thread')
        def doThreadLoop():
            self.locationHash = self.doDecodeGPS()
            while self.runLocationThread:
                report = self.doDecodeGPS()
                self.locationHash.update(report)

        self.locationHash = {}
        self.runLocationThread = True
        self.gpsd = gps(mode=WATCH_ENABLE)

        threading.Thread(target=doThreadLoop).start()

    def stopLocate(self):
        logger.debug('Stopping location thread')
        self.runLocationThread = False

    def doDecodeGPS(self):
        report = None
        while True:
            report = self.gpsd.next()
            logger.debug(report)

            returnHash = {}
            if report['class'] == 'TPV':
                returnHash = self.decodeTPV(report)
                self.TPV_message_received = True
            if report['class'] == 'SKY':
                returnHash = self.decodeSKY(report)
                self.SKY_message_received = True
            return returnHash

    def decodeTPV(self, report):
        returnHash = {}

        try:
            latitude = getattr(report, 'lat', 0.0)
            returnHash['latitude'] = float(abs(math.floor(latitude * 1000000) / 1000000))
            returnHash['latitudeDir'] = 'N' if latitude >= 0 else 'S'

            longitude = getattr(report, 'lon', 0.0)
            returnHash['longitude'] = float(math.floor(longitude * 1000000) / 1000000)
            returnHash['longitudeDir'] = 'E' if longitude >= 0 else 'W'

            timestamp = datetime.strptime(getattr(report, 'time', '2000-01-01T00:00:00.000Z'), "%Y-%m-%dT%H:%M:%S.%fZ") 

            speed = getattr(report, 'speed', 0.0)
            returnHash['groundSpeedKnots'] = float(speed * 1.943844)
            returnHash['course'] = float(getattr(report, 'track', 0.0))

            returnHash['date'] = timestamp.strftime("%y-%m-%d")
            returnHash['time'] = timestamp.strftime("%H:%M:%S")
            returnHash['timestamp'] = timestamp.strftime("%H%M%S.00")

        except:
            logger.exception('Could not decode TPV report')
            raise

        return returnHash

    def decodeSKY(self, report):
        returnHash = {}

        try:
            returnHash["satellitesInView"] = getattr(report, 'nSat', 0)
        except:
            logger.exception('Could not decode SKY report')
            raise

        return returnHash

    def isReady(self):
        return self.TPV_message_received and self.SKY_message_received


    def getLocationHash(self):
        return self.locationHash
