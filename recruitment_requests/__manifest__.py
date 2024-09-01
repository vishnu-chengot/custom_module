# -*- coding: utf-8 -*-
{
    'name': 'Recruitment Request',
    'version': '15.0.0',
    'license': 'OPL-1',
    'category': 'Employees',
    "description": "This module allow department managers to request for new employee recruitment",
    'summary':"Request for new employee recruitment",
    'price': 49,
    'sequence': 1,
    'currency': 'USD',
    'author': "SunArc Technologies",
    'website': 'https://www.suncartstore.com/odoo-apps/recruitment-request',
    'depends': ['base', 'hr_recruitment', 'mail'],
    'images': ['static/description/Banner.png'],
    'data': [
        'data/request_email.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'wizard/start_recruiting.xml',
        'wizard/submit_manager.xml',
        'views/request.xml',
        'views/employee.xml',
        'views/applicant.xml',
    ],
    'installable': True,
    'active': False,
    'application': True
}
