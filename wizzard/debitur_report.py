from odoo import fields, models


class DebiturReport(models.TransientModel):
    _name = 'kredit.debiturreport'
    _description = 'Model untuk reporting PDF Debitur'

    debitur_id = fields.Many2one(
        comodel_name='kredit.debitur', string='Nama Debitur')
    

    def action_debitur_report(self):
        debitur = self.env['kredit.debitur'].search_read([('id', '=', self.debitur_id.id)])
        print("print data debitur")
        print(debitur)
        data = {
            'form': self.read()[0],
            'debiturxx': debitur
        }

        print("print data")
        print(data)
        return self.env.ref('kredit_app.wizzard_debiturreport_pdf').report_action(self, data=data)
