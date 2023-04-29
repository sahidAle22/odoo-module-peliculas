# -*- coding:utf-8 -*-

import logging

from odoo import fields, models, api
from odoo.exceptions import  UserError

logger = logging.getLogger(__name__)

class Presupuesto(models.Model):
    _name = "presupuesto" # name con _ : El verdadero nombre de la clase y el nombre con el que figurará en la base de datos
    _inherit = ["mail.thread","mail.activity.mixin","image.mixin"]

    ## DEFINICIÓN DE LA FUNCIÓN COMPUTE
    @api.depends('detalles_ids')
    def _compute_total(self):
        for record in self:
            sub_total = 0
            for linea in record.detalles_ids:
                sub_total += linea.importe
            record.base = sub_total
            record.impuestos = sub_total * 0.18
            record.total = sub_total * 1.18

    ### LOS CAMPOS DE LA BASE DE DATOS

    name = fields.Char(string="Pelicula") # STRING - VARIABLE DE CARACTERISTICAS ESPECIALES
    active = fields.Boolean(string = "Activo", default = True)  # BOOLEAN - VARIABLE DE CARACTERISTICAS ESPECIALES

    clasificacion = fields.Selection(selection=[ # SELECTION, es un menu desplegable que mostrarà las opciones establecidas
        ('G','G'),          # Publico general
        ('PG','PG'),         # Se recomienda la compañia de un Adulto
        ('PG-13','PG-13'),  # Mayores de 13 años
        ('R','R'),          # Obligatoria la compañia de un Adulto
        ('NC-17','NC-17')   # Mayores de 18
    ], string = "Clasificación")

    dsc_clasificacion = fields.Char(string="Descripción clasificación")
    fch_estreno = fields.Date(string = "Fecha de estreno") #DATE
    puntuacion = fields.Integer(string = "Puntuación", related="puntuacion2")
    puntuacion2 = fields.Integer(string="Puntuación2")

    generos_ids = fields.Many2many(
        comodel_name = "genero", # relacion con el modelo
        string = "Generos"
    )

    director_id = fields.Many2one(
        comodel_name="res.partner",  # este es el nombre que tiene la tabla de la base de datos
        string="Director"
    )  # Existen muchos directores pero solo uno en nuestra pelicula, Relacion muchos a uno

    categoria_director_id = fields.Many2one(
        comodel_name = "res.partner.category",
        string = "Categoria Director",
        default = lambda self: self.env.ref('peliculas.category_director')
    )

    actor_ids = fields.Many2many(
        comodel_name="res.partner",  # este es el nombre que tiene la tabla de la base de datos
        string="Actores"
    )  # Existen muchos directores pero solo uno en nuestra pelicula, Relacion muchos a uno

    categoria_actor_id = fields.Many2one(
        comodel_name="res.partner.category",
        string="Categoria Actor",
        default=lambda self: self.env.ref('peliculas.category_actor')
    )

    vista_general = fields.Text(string = "Descripçión")

    link_trailer = fields.Char(string = "Trailer")

    es_Libro = fields.Boolean(string = "Versión Libro")
    libro = fields.Binary(string = "Libro")
    libro_filename = fields.Char(string="Nombre del libro")

    state = fields.Selection(selection = [
        ('borrador','Borrador'),
        ('aprobado','Aprobado'),
        ('cancelado','Cancelado')
    ], default='borrador', string="Estados", copy=False)

    fch_aprobado = fields.Datetime(string="Fecha Aprobado", copy=False)
    fch_creacion = fields.Datetime(string="Fecha Creación", copy=False, default=lambda self: fields.Datetime.now())
    num_presupuesto = fields.Char(string="Nombre del presupuesto", copy=False)

    opinion = fields.Html(string="Opiniòn")

    detalles_ids = fields.One2many(
        comodel_name = "presupuesto.detalle",
        inverse_name = "presupuesto_id",
        string = "Detalles"
    )

    campos_ocultos = fields.Boolean(string="Campos ocultos")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        default = lambda self: self.env.company.currency_id.id
    )

    terminos = fields.Text(string="Terminos") # Terminos y condiciones
    base = fields.Monetary(string="Total sin Impuestos", compute="_compute_total")
    impuestos = fields.Monetary(string="Impuestos", compute="_compute_total")
    total = fields.Monetary(string="Total", compute="_compute_total") # Base más impuestos


    def aprobar_presupuesto(self):
        logger.info('********** Entro a la función Aprobar Presupuesto')
        self.state = 'aprobado'
        self.fch_aprobado = fields.Datetime.now()

    def cancelar_presupuesto(self):
        self.state = 'cancelado'

    def unlink(self):
        logger.info('********** Entro a la función unlink')
        for record in self:
            if record.state != "cancelado":
                raise UserError("********** NO SE PUEDE ELIMINAR")
            super(Presupuesto, record).unlink()

    @api.model
    def create(self, variables):
        logger.info('********** variables: {0}'.format(variables))

        sequence_obj = self.env['ir.sequence']
        correlativo = sequence_obj.next_by_code('secuencia.presupuesto.pelicula')
        variables['num_presupuesto'] = correlativo
        print(variables)
        return super(Presupuesto,self).create(variables)

    def write(self, variables):
        logger.info('********** variables: {0}'.format(variables))
        print(variables)
        #if 'clasificacion' in variables:
        #    raise UserError('La clasificación no se puede editar')
        return super(Presupuesto, self).write(variables)

    def copy(self, default=None):
        default = dict(default or {})
        default["name"] = self.name + " (Copia)"
        default["puntuacion2"] = 1

        return super(Presupuesto,self).copy(default)

    @api.onchange('clasificacion')
    def _onchange_clasificacion(self):
        if self.clasificacion:
            if self.clasificacion == 'G':
                self.dsc_clasificacion = "Publico general"
            if self.clasificacion == 'PG':
                self.dsc_clasificacion = "Se recomienda la compañia de un Adulto"
            if self.clasificacion == 'PG-13':
                self.dsc_clasificacion = "Mayores de 13 años"
            if self.clasificacion == 'R':
                self.dsc_clasificacion = "Obligatoria la compañia de un Adulto"
            if self.clasificacion == 'NC-17':
                self.dsc_clasificacion = "Mayores de 18"
        else:
            self.dsc_clasificacion = False


class PresupuestoDetalle(models.Model):
    _name = "presupuesto.detalle"

    presupuesto_id = fields.Many2one(
        comodel_name = "presupuesto",
        string = "Presupuesto"
    )

    # CAMPOS DE RECURSOS CINEMATOGRAFICOS

    name = fields.Many2one( # este apunta a la tabla/modelo recurso.cinematografico
        comodel_name = "recurso.cinematografico",
        string = "Recursos"
    )

    descripcion = fields.Char(string="Descripcion", related = "name.descripcion")
    contacto_id = fields.Many2one(
        comodel_name = "res.partner",
        string = "Contacto",
        related = "name.contacto_id"
    )

    imagen = fields.Binary(string="Imagen", related="name.imagen")


    # CAMPOS PROPIOS
    cantidad = fields.Float(string="Cantidad", default=1.0, digits=(16,4))
    precio = fields.Float(string="Precio", digits="Product Price")
    importe = fields.Monetary("Importe")

    currency_id = fields.Many2one(
        comodel_name="res.currency",
        string="Moneda",
        related="presupuesto_id.currency_id"
    )

    @api.onchange('name')
    def _onchange_name(self):
        if self.name: # Si no está vacio
            self.precio = self.name.precio

    @api.onchange('precio','cantidad')
    def _onchange_importe(self):
        if self.name:
            self.importe = self.cantidad * self.precio