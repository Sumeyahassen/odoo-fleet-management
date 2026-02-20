{
    'name': 'Fleet Customizations',
    'version': '1.0',
    'category': 'Fleet',
    'summary': 'Custom fleet management with trip logging',
    'depends': ['fleet'],
        'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'views/fleet_trip_views.xml',
    ],
    'installable': True,
    'application': False,
}