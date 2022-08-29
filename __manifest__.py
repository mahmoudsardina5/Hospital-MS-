# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'MS',
    'category': 'Website',
    'summary': 'new in odoo ',
    'version': '1.0',
    'description': """
        Test
        """,
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'reports/report.xml',
        'reports/patient_card.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
