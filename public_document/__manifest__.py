{
    'name': 'Public Document',
    'version': '15.0.0.0',
    'category': 'Document Management',
    'author': 'Doyenhub Software Solution',
    'company': 'Doyenhub Software Solution',
    'maintainer': 'Doyenhub Software Solution',
    'sequence': -100,
    'summary': 'This app allows the admin user to upload documents along with descriptions and additional details. These documents can then be accessed and utilized by all users who have permission to view them.',
    'description': """This app allows the admin user to upload documents along with descriptions and additional details. These documents can then be accessed and utilized by all users who have permission to view them.""",
    'depends':['base','mail'],
    'data': [
        'security/document_security.xml',
        'security/ir.model.access.csv',
        'views/menu.xml',
        ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    "images":['static/description/images/banner.png'],
    'assets': {},
    'website':'https://www.doyenhub.com/',
}


