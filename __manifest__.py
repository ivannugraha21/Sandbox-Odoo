# -*- coding: utf-8 -*-
{
    'name': "restapi",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    #
    'auto_install': True,
    # any module necessary for this one to work correctly
    'depends': ['base', 'sale_management', 'sale', 'product', 'account_accountant', 'account', 'stock', 'purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #
        'data/scheduler_sandbox.xml',
        #
        'views/views.xml',
        'views/templates.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/sale_product_views.xml',
        'views/res_users_views.xml',
        'views/sale_order_views.xml',
    ],
    'assets':  {
        'web.assets_backend': [
            'restapi/static/src/js/newAttrButtonVisible.js',
            #'restapi/static/src/js/btnUpdateProductList.js',
            #'restapi/static/src/js/btnUpdateProductKanban.js',
        ],
        'web.assets_qweb': [
            #'restapi/static/src/xml/custom_button.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
