from odoo import fields, models, api


class MedicalTest(models.Model):
    _name = 'dv.medicaltest'
    _description = 'Hospital MedicalTest'

    name = fields.Char(string='Tên dịch vụ khám', required=True)
    price = fields.Integer(string= 'Giá dịch vụ', required=True)
    medical_test_ids = fields.Many2many(comodel_name='dv.appointment', relation='medicaltest_appointment_rel',
                                        column1='medicaltest_id', column2='appointment_id')

