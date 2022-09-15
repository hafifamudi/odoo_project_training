from odoo import api, fields, models


class Kreditur(models.Model):
    _name = 'kredit.kreditur'
    _description = 'Model untuk menampung data orang-orang yang meminjamkan uang'
    _rec_name = 'kreditur_name'

    kreditur_name = fields.Char(string='Nama')
    kreditur_status = fields.Selection([
        ('kreditur_active', 'Active'),
        ('kreditur_inactive', 'Inactive')
    ], string='Kreditur Status', 
    readonly=True, required=True, default='kreditur_active')
    total_debitur = fields.Integer(string='Total Debitur', compute='_compute_total_debitur')
    total_barang = fields.Integer(string='Total Barang Lelang', compute='_compute_total_barang')
    debitur_ids = fields.One2many(
        comodel_name='kredit.debitur', 
        inverse_name='kreditur_id', 
        string='Debitur')
    barang_ids = fields.One2many(
        comodel_name='kredit.barang', 
        inverse_name='kreditur_id', 
        string='Barang Lelang')

    @api.depends('barang_ids')
    def _compute_total_barang(self):
        for record in self:
            record.total_barang = self.env['kredit.barang'].search_count([('kreditur_id', '=', record.id)])
    
    @api.depends('debitur_ids')
    def _compute_total_debitur(self):
        for record in self:
            record.total_debitur = self.env['kredit.debitur'].search_count([('kreditur_id', '=', record.id)])
    
    def action_active(self):
        self.write({'kreditur_status' : 'kreditur_active'})
    
    def action_inactive(self):
        self.write({'kreditur_status' : 'kreditur_inactive'})
        
