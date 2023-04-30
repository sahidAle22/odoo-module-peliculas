# -*- coding:utf-8 -*-
from odoo.http import Controller, request, route, Response
from odoo import http
import json
CORS = '*'

class PresupuestoController(Controller):

    @route('/api/presupuesto', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_presupuestos(self):
        campos = ['name','puntuacion','clasificacion','generos_ids','director_id','detalles_ids','vista_general','link_trailer']
        presupuestos = request.env['presupuesto'].sudo().search_read([],campos)
        return Response(json.dumps(presupuestos), content_type='application/json', status=200)

    @route('/api/presupuesto/<int:presupuesto_id>', type='http', auth='public', cors='*', csrf=False,  methods=['GET'])
    def get_presupuesto(self, presupuesto_id, **kwargs):
        campos = [
            'name',
            'puntuacion',
            'clasificacion',
            'generos_ids',
            'actor_ids',
            'director_id',
            'detalles_ids',
            'vista_general',
            'link_trailer',
            'num_presupuesto',
            'fch_creacion'
        ]

        presupuesto = request.env['presupuesto'].sudo().search_read([('id', '=', presupuesto_id)],campos)

        if not presupuesto:
            return Response(json.dumps({'error': 'El presupuesto no existe'}), status=404, content_type='application/json')

        generos = request.env['genero'].sudo().search_read([])
        generoData = []
        for genero in generos:
            if genero['id'] in presupuesto[0]['generos_ids']:
                generoData.append({"id": genero['id'], "name": genero['name']})

        actores = http.request.env['res.partner'].sudo().search_read([('category_id', '=', 'Actor')], ['name'])
        actorData = []
        for actor in actores:
            if actor['id'] in presupuesto[0]['actor_ids']:
                actorData.append({"id": actor['id'], "name": actor['name']})

        presupuesto[0]['actor_ids'] = actorData
        presupuesto[0]['generos_ids'] = generoData
        presupuesto[0]['fch_creacion'] = presupuesto[0]['fch_creacion'].strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return Response(json.dumps(presupuesto[0]), content_type='application/json', status=200)

    @route('/api/presupuesto/crear',type='json', auth='public', cors='*', csrf=False, methods=['POST','OPTIONS'])
    def create_presupuesto(self, **params):
        if request.httprequest.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': 'http://localhost:5173',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true',
            }
            return '', 200, headers

        if ('name' not in params) or ('clasificacion' not in params):
            return {'error': 'Faltan parametros obligatorios'}, 500

        new_presupuesto = request.env['presupuesto'].sudo().create(params)
        return {'id': new_presupuesto.id, 'name': new_presupuesto.name}, 200

    @route('/api/presupuesto/actualizar', type='json', auth='none', cors='*', methods=['POST','OPTIONS'], csrf=False)
    def update_presupuesto(self, **params):
        if request.httprequest.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': 'http://localhost:5173',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            }
            return '', 200, headers


        id = params['idPresupuesto']
        del params['idPresupuesto']
        params['generos_ids'] = [[6, False, params['generos_ids']]]
        params['actor_ids'] = [[6, False, params['actor_ids']]]

        presupuesto = request.env['presupuesto'].sudo().search([('id', '=', id)])

        if not presupuesto:
            return {'error': 'No existe el presupuesto'}, 404

        presupuesto.sudo().write(params)
        updated_presupuesto = request.env['presupuesto'].browse(id)
        return json.dumps({'id': updated_presupuesto.id, 'name': updated_presupuesto.name}), 200

    @http.route('/api/presupuesto/eliminar', auth='none', type='json', cors=CORS, methods=['POST','OPTIONS'], csrf=False)
    def delete_presupuesto(self, **params):
        if request.httprequest.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': 'http://localhost:5173',
                'Access-Control-Allow-Methods': 'GET,POST,OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization',
                'Access-Control-Allow-Credentials': 'true',
            }
            return '', 200, headers

        if params['idPresupuesto']:
            presupuesto = request.env['presupuesto'].sudo().search([('id', '=', params['idPresupuesto'])])
            if presupuesto:
                presupuesto.action_archive()
                return  {
                    "code": 201,
                    "message": 'Delete'
                }
            else:
                detalle = 'Este presupuesto no existe o ya fue archivado'
                return {
                    "code": 400,
                    "message": detalle,
                    "data": params['idPresupuesto']
                }

    @http.route('/api/generos', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_generos(self):
        campos = ['name']
        generos = http.request.env['genero'].sudo().search_read([], campos)
        return Response(json.dumps(generos), content_type='application/json', status=200)

    @http.route('/api/directores', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_Directores(self):
        campos = ['name']
        presupuestos = http.request.env['res.partner'].sudo().search_read([('category_id','=','Director')], campos)
        return Response(json.dumps(presupuestos), content_type='application/json', status=200)

    @http.route('/api/actores', type='http', auth='public', cors='*', csrf=False, methods=['GET'])
    def get_Actores(self):
        campos = ['name']
        presupuestos = http.request.env['res.partner'].sudo().search_read([('category_id', '=', 'Actor')], campos)
        return Response(json.dumps(presupuestos), content_type='application/json', status=200)