# -*- coding:utf-8 -*-

from odoo import fields, models, api

class Genero(models.Model):
    _name = "genero" # nombre de la tabla en la BD

    name = fields.Char()
