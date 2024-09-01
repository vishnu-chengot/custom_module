{
    'name': 'Sale order list view - Sales Profit and Loss Preview.',
    'summary': """Sale order list view - Sales Profit and Loss Preview.""",
    'version': '15.0',
    'license': "LGPL-3",
    'description': """Sale order list view - Sales Profit and Loss Preview.Sale order preview including - Margin by line items, Total Margin, Invoice details, Invoice dues,Payment dues.""",
    'author': 'Arun Reghu Kumar',
    'company': 'Tech4Logic',
    'website': 'https://tech4logic.wordpress.com/',
    'category': 'HR',
    'depends': ['base', 'sale'],
    'data': [
            'views/sales_profit_view.xml',
        ],
    'qweb': [],
    'assets': {
        'web.assets_backend': [
            'sales_profit/static/src/js/sales_profit.js'
        ],
        'web.assets_qweb': [
            'sales_profit/static/src/xml/sales_profit_select.xml'
        ],
    },
    'images': ['static/description/banner.gif'],
    'demo': [],
    'installable': True,
    'auto_install': False,

}
