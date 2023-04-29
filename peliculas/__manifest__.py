# -*- coding:utf-8 -*-

{
    'name': 'Modulo de peliculas',
    'version': '1.0',
    'depends': [
        'contacts',
        'mail',
    ],
    'author': 'Sahid Alejandro',
    'category':  'Peliculas',
    'website': 'http://www.google.com',
    'summary': 'Modulo de presupuestos para peliculas',
    'description': 'Modulo para hacer presupuestos de peliculas',
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/secuencia.xml',
        'data/categoria.xml',
        'wizard/update_wizard_views.xml',
        'report/reporte_pelicua.xml',
        'views/menu.xml',
        'views/presupuesto_views.xml'
    ],
}