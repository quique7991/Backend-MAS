from bson.objectid import ObjectId
import logging
from math import pow,sqrt
from tornado.gen import Return, coroutine
from urllib2 import urlopen
import config
import boxer
import calendar
from datetime import datetime
from geoutils import *

class _SelectRoute:
    '''
    ***************************************************************************
                                Select Route
    ***************************************************************************
    '''
    @coroutine
    def set_route(self,idUser,route_index):
        erase_result = yield self.db.persons.remove({'uid':idUser,'index':{'$ne':route_index}})
        result = yield self.db.persons.update({'uid':idUser,'index':route_index},{'temporal':False})
        raise Return(result)

    @coroutine
    def update_route(self,idUser,route_index,position,radius):
        temp_result = yield self.db.persons.find({'uid':idUser,'index':route_index,'loc':{'$nearSphere':{'$geometry':{'type':'Point','coordinates':[float(position['lng']),float(position['lat'])],'$maxDistance':float(radius)}}}}).to_list(length=int(1))
        result = {}
        logging.info(temp_result)
        if temp_result:
            utc_now = self.obtain_utc_time()    
            value = temp_result[0]
            utc_initial = value['initial']
            delta = utc_now-utc_initial
            result = yield self.db.persons.update({'uid':idUser,'index':route_index,'initial':{'$ge':utc_initial}},{'$inc':{'initial':delta,'finish':delta}})
        else:
            result['success']=False
        raise Return(result)
        #Calculate the vlaue and the weight for each route, normalized for each route.
        
    def obtain_utc_time(self):
        time_now = datetime.now()
        if time_now.utcoffset() is not None:
            time_now = time_now - time_now.utcoffset()
        millis = int(calendar.timegm(time_now.timetuple())*1000+time_now.microsecond/1000)
        return millis




