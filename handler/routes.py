from base import BaseHandler
import json
from bson import json_util
import tornado.web

class Route(BaseHandler):
    SUPPORTED_METHODS='GET,POST'
#TODO: User should be logged
#    @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self):
#        idUser = self.current_user['_id']
        idUser = 1
        starting_point = self.get_argument("dest")
        destination_point = self.get_argument("start")
        starting_point = eval(starting_point)
        destination_point = eval(destination_point)
        model = self.settings['model']
        response = yield model.get_route(idUser,destination_point,starting_point)
        if response:
            self.write(json.dumps({'success': True,'response':response},default=json_util.default))
        else:
            self.write({'success': False})
        return

#TODO: User should be logged
#    @tornado.web.authenticated
    @tornado.gen.coroutine
    def post(self):
    #        idUser = self.current_user['_id']
        idUser = 1
        current_position = self.get_argument("current_position")
        route_index = self.get_argument("route_index")
        radius = self.get_argument("radius",5000)
        current_position = eval(current_position)
        model = self.settings['model']
        response = yield model.update_route(idUser,route_index,current_position,radius)
        if response:
            self.write(json.dumps({'success': True,'response':response},default=json_util.default))
        else:
            self.write({'success': False})
        return

