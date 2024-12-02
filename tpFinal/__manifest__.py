{
    'name': "Custom Sales and Employees Management",
    'version': '1.0',
    'summary': "Manages employee workloads and customizes invoices",
    'author': "Your Name",
    'depends': ['sale', 'hr', 'account'],
    'data': [
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'views/employee_form.xml',
        'views/report_invoice_document.xml',
        'report/report.xml',
        'views/report_saleorder_document_inherit.xml',
        'menu/sale_order_actions.xml',
        'menu/sale_order_menu.xml',
    ],
    'installable': True,
    'application': True,
}
