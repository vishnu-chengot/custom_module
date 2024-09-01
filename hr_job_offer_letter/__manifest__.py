{
    'name': 'Job Offer Letter',
    'version': "1.0.0",
    "author": "Odoo Bangladesh",
    "website": "http://odoobangladesh.com",
    'category': 'Human Resources',
    'depends': ['hr_recruitment'],
    'data': [
        'data/mail_data.xml',
        'views/he_application_send_mail_btn.xml',
    ],
    'installable': True,
    'application': False,
}
