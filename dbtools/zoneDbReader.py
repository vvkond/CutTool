# -*- coding: utf-8 -*-

# Qt import
from qgis.PyQt import uic, QtCore, QtGui, QtXml

# qgis import
import qgis
from qgis.core import *
from qgis.gui import *
import numpy
from math import sqrt

from .dbReaderBase import *

class ZoneDbReader(DbReaderBase):

    def __init__(self, iface, parent=None):
        DbReaderBase.__init__(self, iface, parent)

    def readZone(self, well_sldnid, zonationId, zoneId):
        if not self.initDb():
            return None

        zones = self.db.execute(self.get_sql('zone.sql'), wellId=well_sldnid, zonation_id=zonationId, zone_id=zoneId)
        if not zones:
            return None

        zones = []
        for row in zones:
            if row[3] and row[4]:
                zones.append((row[1]+'/'+row[2], row[3], row[4]))

        return zones
