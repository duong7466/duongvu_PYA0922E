from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime
import re


class Patient(models.Model):
    _name = 'dv.patient'
    _description = 'Hospital Patient'

    name = fields.Char(string='Tên bệnh nhân', required=True)
    address = fields.Char(string='Địa chỉ')
    gender = fields.Selection(string='Giới tính',
                              selection=[('male', 'Nam'), ('female', 'Nữ')], default='male')
    phone = fields.Char(string='Số điện thoại', required=True)
    dob = fields.Date(string='Ngày tháng năm sinh', required=True)
    email = fields.Char(string='Địa chỉ email', required=True)
    age = fields.Integer(string='Tuổi')
    patient_appointment_ids = fields.One2many(comodel_name='dv.appointment', inverse_name='patient_id',
                                             string='Cuộc hẹn')
    total_appointments = fields.Integer(string='Tổng số cuộc hẹn', compute='_get_total_appointments', stored=True)

    @api.onchange('dob')
    def onchange_dob(self):
        domain = {'department_id': []}
        if self.dob:
            current_year = datetime.now().year
            birth_year = self.dob.year
            if birth_year > current_year:
                return {
                    'warning': {
                        'title': 'Cảnh báo !',
                        'message': 'Ngày sinh không hợp lệ !'
                    },
                    'domain': domain,
                }
            self.age = current_year - self.dob.year
        return {'domain': domain}


    @api.constrains('name', 'phone')
    def _check_patient_exists(self):
        for record in self:
            patient = self.env['dv.patient'].search(
                [('name', '=', record.name), ('phone', '=', record.phone), ('id', '!=', record.id)])
            if patient:
                raise ValidationError(f'Bệnh nhân {record.name} đã tồn tại')

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            valid_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                   record.email)
            if valid_email is None:
                raise ValidationError('Vui lòng nhập địa chỉ Email hợp lệ')

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(Patient, self).create(vals)

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(Patient, self).write(vals)

    def _get_total_appointments(self):
        for record in self:
            record.total_appointments = self.env['dv.appointment'].search_count([('patient_id', '=', record.id)])










