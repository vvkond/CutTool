# -*- coding: utf-8 -*-

# Qt import
from qgis.PyQt import uic, QtCore, QtGui, QtXml

# qgis import
import qgis
from qgis.core import *
from qgis.gui import *
import fnmatch

from .dbReaderBase import *

class ZoneDbReader(DbReaderBase):

    def __init__(self, iface, parent=None):
        DbReaderBase.__init__(self, iface, parent)

    def readZonationByDesc(self, descPattern):
        if not self.initDb():
            return 0

        patterns = [x.strip() for x in descPattern.split(',')]

        rows = self.db.execute(self.get_sql('zonation.sql'))
        zonationId = 0

        if rows:
            for row in rows:
                val = row[1]
                vals = [val for w in patterns if fnmatch.fnmatch(val, w)]
                if len(vals) > 0:
                    zonationId = int(row[0])
                    break

        return zonationId

    def readZonationLatestForWell(self, well_sldnid):
        if not self.initDb():
            return 0

        rows = self.db.execute(self.get_sql('zonation_latest.sql'), wellId=well_sldnid)
        zonationId = 0

        if rows:
            for row in rows:
                zonationId = int(row[0])
                break

        return zonationId

    def readZone(self, well_sldnid, zonationId):
        if not self.initDb():
            return None

        rows = self.db.execute(self.get_sql('zone.sql'), wellId=well_sldnid, zonation_id=zonationId)
        if not rows:
            return None

        zones = []
        for row in rows:
            # print row[0], row[1], row[2]
            if row[3] and row[4]:
                zones.append((row[1]+'/'+row[2], row[3], row[4]))

        return zones
