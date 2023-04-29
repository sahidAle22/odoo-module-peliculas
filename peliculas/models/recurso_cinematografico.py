# -*- coding:utf-8 -*-

from odoo import fields, models, api

class RecursoCinematografico(models.Model):
    _name = "recurso.cinematografico" # usar . para tener varias palabras en el _name

    name = fields.Char(string="Recurso")
    descripcion = fields.Char(string="Descripcion")
    precio = fields.Char(string="Precio")
    contacto_id = fields.Many2one(
        comodel_name = "res.partner",
        domain = "[('is_company','=',False)]"
    )

    imagen = fields.Binary(string="Imagen")
