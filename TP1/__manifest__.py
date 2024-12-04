{
    'name': 'Sales Analytics',
    'version': '1.0',
    'summary': 'Analyse des ventes, gestion des saisons, produits, fidélité client, performance des employés et recommandations',
    'depends': ['sale', 'hr', 'product','base'],
    'data': [
        'security/groupe.xml',
        'security/ir.model.access.csv',
        'views/season_views.xml',
        'views/product_performance_views.xml',
        'views/customer_views.xml',
        'views/employee_views.xml',
        'views/satisfaction_views.xml',
        'views/recommendation_views.xml',
        'views/actions.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'application': True,
}
