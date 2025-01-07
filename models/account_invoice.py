from odoo import models, fields, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    mensaje_activo = fields.Boolean(string='Activo')
    cotizacion_dolar = fields.Monetary(string='Cotizacion', currency_field='currency_id')
    total_dolares = fields.Monetary(string='Total Dolares', currency_field='currency_id')
    mensaje_invoice = fields.Text(string='Mensaje Invoice', compute='_compute_mensaje_invoice')

    report_amount_iva_content = fields.Monetary(
        string='IVA Content',
        compute='_compute_report_amount_iva_content'
    )

    report_amount_other_taxes = fields.Monetary(
        string='Other Taxes Content',
        compute='_compute_report_amount_iva_content'
    )

    @api.depends(
        'amount_untaxed', 'amount_tax', 'tax_line_ids', 'document_type_id')
    def _compute_report_amount_iva_content(self):
        for invoice in self:
            tot_iva = 0
            tot_other = 0
            for tax in invoice.tax_line_ids:
                if 'IVA' in tax.tax_id.name:
                    tot_iva += tax.amount
                else:
                    tot_other += tax.amount
            invoice.report_amount_iva_content = tot_iva
            invoice.report_amount_other_taxes = tot_other


    @api.one
    @api.depends('currency_id')
    def _compute_mensaje_invoice(self):
        self.mensaje_invoice = '''La presente factura fue emitida a una cotización dólar TARJETA de $ %.2f
Siendo el total de la misma la cantidad de U$S  %.2f
La misma debe ser cancelada dentro de las 72hs hábiles fecha de factura según condición de venta pactada, caso contrario será refacturada a una nueva cotización vigente.
        ''' % (self.cotizacion_dolar, self.total_dolares)

