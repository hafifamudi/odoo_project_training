from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


class Barang(models.Model):
    _name = 'kredit.barang'
    _description = 'Model untuk menampung data barang yang di lelang'
    _rec_name = 'barang_name'

    barang_name = fields.Char(string='Nama')
    barang_photo = fields.Binary(string='Foto Barang')

    barang_status = fields.Selection([
        ('barang_bid_process', 'Bid Process'),
        ('barang_sold', 'Sold')
    ], string='Status Pelelangan', readonly=True, required=True, default='barang_bid_process')
    barang_masa_aktif = fields.Selection([
        ('barang_out_of_date', 'Out Of Date'),
        ('barang_in_of_date', 'In Of Date')
    ], string='Status Kadaluwarsa', 
        readonly=True, required=True, default='barang_in_of_date', compute='_compute_barang_masa_aktif')

    barang_due_date = fields.Date(string='Tanggal Akhir Lelang')
    total_partisipan_lelang = fields.Integer(string='Total Partisipan Lelang', 
                                            compute='_compute_total_partisipan_lelang')
    
    kreditur_id = fields.Many2one(
        comodel_name='kredit.kreditur', 
        string='Pelelang')
    user_id = fields.Many2many(
        comodel_name='kredit.userlelang', 
        string='Pengikut Lelang')
    
    @api.depends('user_id')
    def _compute_total_partisipan_lelang(self):
        for record in self:
            record.total_partisipan_lelang = self.env['kredit.userlelang'].search_count([('barang_id', '=', record.id)])
    
    @api.depends('barang_due_date')
    def _compute_barang_masa_aktif(self):
       for record in self:
        if datetime.date(fields.datetime.now()) > record.barang_due_date:
            record.barang_masa_aktif = 'barang_out_of_date'
        else:
            record.barang_masa_aktif = 'barang_in_of_date'
    
    @api.onchange('kreditur_id')
    def _onchange_kreditur_id(self):
        if self.kreditur_id.kreditur_status == 'kreditur_inactive':
            raise UserError('{} berstatus Inactive. Mohon untuk memilih Kreditur Lainnya.'.format(self.kreditur_id.kreditur_name))

    def action_sold(self):
        self.write({'barang_status' : 'barang_sold'})

    def action_bid(self):
        self.write({'barang_status' : 'barang_bid_process'})
    
