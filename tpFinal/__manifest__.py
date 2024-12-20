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
        'report/report_action.xml',
        'report/invoice_template.xml',
        'data/ir_config_parameter_data.xml',
        'views/account_move_view.xml',
        'views/payment_method_rule_views.xml',
        'views/res_config_settings_views.xml',
        'menu/sale_order_actions.xml',
        'menu/sale_order_menu.xml',
    ],
    'installable': True,
    'application': True,
}
