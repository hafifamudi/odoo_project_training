# -*- coding: utf-8 -*-
from odoo import http, models, fields
from odoo.http import request
import json

class Credito(http.Controller):
    @http.route('/kredito/getDebitur', auth='public', method=['GET'])
    def getBarang(self, **kwargs):
        list_debitur = request.env['kredit.debitur'].search([])
        val = []
        for ktr in list_debitur:
            val.append({
                'nama_debitur': ktr.debitur_name,
                'pekerjaan_debitur': ktr.debitur_job,
                'nomor_hp_debitur': ktr.debitur_phone_number,
                'status_pelunasan_debitur': ktr.debitur_status
            })
        return json.dumps(val)

    @http.route('/kredito/getKreditur', auth='public', method=['GET'])
    def getSupplier(self, **kwargs):
        list_kreditur = request.env['kredit.kreditur'].search([])
        val = []
        for ktr in list_kreditur:
            val.append({
                'nama_kreditur': ktr.kreditur_name,
                'status_kreditur': ktr.kreditur_status,
                'total_debitur_kreditur': ktr.total_debitur,
                'total_barang_kreditur': ktr.total_barang
            })
        return json.dumps(val)