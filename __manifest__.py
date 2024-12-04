{
    'name': 'Gestion des Factures Personnalisées',
    'version': '1.0',
    'category': 'Sales',
    'author': 'me',
    'depends': ['sale', 'hr', 'account'],
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/employee_form.xml',
        'report/report_action.xml',
        'report/invoice_template.xml',
        'menu/sale_order_actions.xml',
        'menu/sale_order_menu.xml',
    ],
    'installable': True,
    'application': True,
}
