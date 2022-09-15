from datetime import datetime
from odoo import fields, models, api
from odoo.exceptions import ValidationError, UserError


class Debitur(models.Model):
    _name = 'kredit.debitur'
    _description = 'Model untuk menampung data user yang melakukan peminjaman uang'
    _rec_name = 'debitur_name'
    debitur_name = fields.Char(string='Nama', required=True)
    debitur_ktp = fields.Binary(string='KTP', required=True)
    debitur_photo = fields.Binary(string='Foto Profil', required=True)
    debitur_job = fields.Char(string='Pekerjaan', required=True)
    debitur_phone_number = fields.Char(string='Nomor Telepon', required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status Peminjaman', readonly=True, required=True, default='draft')
    debitur_status = fields.Selection([
        ('debitur_belum_lunas', 'Belum Lunas'),
        ('debitur_sudah_lunas', 'Sudah Lunas'),
    ], string='Status Pelunasan', required=True, default='debitur_belum_lunas')
    debitur_status_waktu = fields.Selection([
        ('debitur_belum_jatuh_tempo', 'Belum Jatuh Tempo'),
        ('debitur_sudah_jatuh_tempo', 'Sudah Jatuh Tempo'),
    ], string='Status Waktu Peminjaman', readonly=True, required=True, default='debitur_belum_jatuh_tempo', compute='_compute_debitur_status_waktu')
    
    debitur_borrow_date = fields.Date(string='Tanggal Peminjaman', required=True)
    debitur_due_date = fields.Date(string='Tanggal Jatuh Tempo', required=True)
    debitur_total_borrow = fields.Integer(string='Total Pinjaman')
    kreditur_id = fields.Many2one('kredit.kreditur', string='Nama Kreditur', ondelete='cascade', required=True)
    
    @api.depends('debitur_due_date')
    def _compute_debitur_status_waktu(self):
       for record in self:
        if datetime.date(fields.datetime.now()) > record.debitur_due_date:
            record.debitur_status_waktu = 'debitur_sudah_jatuh_tempo'
        else:
            record.debitur_status_waktu = 'debitur_belum_jatuh_tempo'

    @api.onchange('kreditur_id')
    def _onchange_kreditur_id(self):
        if self.kreditur_id.kreditur_status == 'kreditur_inactive':
            raise UserError('{} berstatus Inactive. Mohon untuk memilih Kreditur Lainnya.'.format(self.kreditur_id.kreditur_name))

    @api.constrains('debitur_total_borrow')
    def _constrains_quantity(self):
        for rec in self:
            if rec.debitur_total_borrow == 0:
                raise ValidationError("Mohon untuk memasukan total pinjaman yang akan di ajukan")

    @api.model
    def create(self, vals):
        debitur_name = vals.get('debitur_name')
        get_status_peminjaman = self.env['kredit.debitur'].search([('debitur_name', '=', debitur_name)]).mapped('debitur_status')
        
        if get_status_peminjaman[0] == 'debitur_belum_lunas':
            raise UserError('{} mohon melakukan pelunasan terlebih dahulu!'.format(debitur_name))
        else:
            return super().create(vals)

    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_pending(self):
        self.write({'state': 'pending'})

    def action_approved(self):
        self.write({'state': 'approved'})

    def action_rejected(self):
        self.write({'state': 'rejected'})


    
