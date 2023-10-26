from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    mensaje_activo = fields.Boolean(string='Activo')
    cotizacion_dolar = fields.Monetary(string='Cotizacion', currency_field='currency_id')
    total_dolares = fields.Monetary(string='Total Dolares', currency_field='currency_id')
    mensaje_invoice = fields.Text(string='Mensaje Invoice', compute='_compute_mensaje_invoice')


    @api.one
    @api.depends('currency_id')
    def _compute_mensaje_invoice(self):
        self.mensaje_invoice = '''La presente factura fue emitida a una cotización dólar TARJETA de $ %.2f
Siendo el total de la misma la cantidad de U$S  %.2f
La misma debe ser cancelada dentro de las 72hs hábiles fecha de factura según condición de venta pactada, caso contrario será refacturada a una nueva cotización vigente.
        ''' % (self.cotizacion_dolar, self.total_dolares)

