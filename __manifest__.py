# -*- coding: utf-8 -*-
{
    'name': "Credito",
    'summary': "Aplikasi pinjam uang yang cepat, tanggap dan responsif",
    'author': "Hafif Nur Muhammad",
    'category': 'services/credito',
    'version': '0.1',
    'depends': ['base', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'wizzard/debiturreport_wizzard_view.xml',
        'views/menu.xml',
        'views/barang_view.xml',
        'views/debitur_view.xml',
        'views/kreditur_view.xml',
        'views/barang_view.xml',
        'views/user_lelang_view.xml',
        'report/report.xml',
        'report/wizzard_debiturreport_template.xml'
    ],
}
