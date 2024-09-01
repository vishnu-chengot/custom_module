from odoo import api, fields, models
from datetime import date
from odoo.exceptions import AccessError

class PublicDocument(models .Model):
    _name = "public.document"
    _inherit = ['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string='Title',tracking=True,required=True)
    tag = fields.Many2many('document.tag',string='Tags',tracking=True,required=True)
    description = fields.Html(string='Description')
    document_file = fields.Many2many('ir.attachment',string="Upload Document", tracking=1)
    author = fields.Many2one('hr.employee', string='Author',tracking=True ,required=True)

    @api.model
    def create(self, vals):
        templates = super(PublicDocument,self).create(vals)
        # fix attachment ownership and  access issse for this
        for template in templates:
            if template.document_file:
                template.document_file.write({'res_model': self._name, 'res_id': template.id})
        return templates