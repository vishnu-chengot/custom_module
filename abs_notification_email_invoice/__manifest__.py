# -*- coding: utf-8 -*-
#################################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2021-today Ascetic Business Solution <www.asceticbs.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#################################################################################
{
    'name': "Notification Email From Invoice",
    'author': 'Ascetic Business Solution',
    'category': 'sales',
    'summary': """Notification Email From Invoice""",
    'website': 'http://www.asceticbs.com',
    'description': """ """,
    'version': '15.0.1.0',
    'depends': ['base','sale_management','purchase'],
    'data': ['views/account_invoice_view.xml','views/scheduler_in_account_invoice.xml'],
    'images': ['static/description/banner.png'],
    'license': 'AGPL-3',
    'installable': True,
    'application': True,
    'auto_install': False,
}
