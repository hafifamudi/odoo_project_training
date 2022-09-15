from odoo import api, fields, models
from odoo.exceptions import UserError


class UserLelang(models.Model):
    _name = 'kredit.userlelang'
    _description = 'Model untuk menampung data para user yang mengikuti lelang barang'
    _rec_name = 'user_name'
    user_name = fields.Char(string='Nama')
    user_address = fields.Char(string='Alamat')
    user_phone_number = fields.Char(string='Nomor Telepon')
    user_photo = fields.Binary(string='Foto Profil')
    user_bid = fields.Integer(string='Penawaran Harga')
    barang_id = fields.Many2many(
        comodel_name='kredit.barang', string='Barang Lelang')
    
    @api.constrains('barang_id')
    def _constrains_user_id(self):
        for record in self:
            if record.barang_id.barang_status == 'barang_sold' or\
                record.barang_id.barang_masa_aktif == 'barang_out_of_date':
                raise UserError("{} sudah terjual atau out of date, silahkan mengikuti barang lelang yang lainnya.".format(record.barang_id.barang_name))

    
    
    
