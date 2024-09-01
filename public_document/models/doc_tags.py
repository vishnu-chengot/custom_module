from odoo import api, fields, models
from datetime import date

class DocTag(models .Model):
    _name = "document.tag"
    _rec_name='tag'
    
    tag = fields.Char(string='Tags')

