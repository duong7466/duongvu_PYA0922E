from odoo import fields, models, api
from datetime import datetime
from odoo.exceptions import ValidationError
import re


class Doctor(models.Model):
    _name = 'dv.doctor'
    _description = 'Hospital Doctor'

    name = fields.Char(string='Tên bác sĩ', required=True)
    description = fields.Text(string='Mô tả')
    address = fields.Char(string='Địa chỉ')
    gender = fields.Selection(string='Giới tính',
                              selection=[('male', 'Nam'), ('female', 'Nữ')], default='male')
    phone = fields.Char(string='Số điện thoại', required=True)
    email = fields.Char(string='Địa chỉ email', required=True)
    joined_from = fields.Date(string='Ngày bắt đầu công việc')
    image_1920 = fields.Image(string='Ảnh đại diện', max_width=1920, max_height=1920)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128, store=True)
    state = fields.Selection(string='Hợp đồng làm việc',
                              selection=[('fulltime', 'Toàn thời gian'), ('parttime', 'Bán thời gian')],
                              default='fulltime', required=True)
    dob = fields.Date(string='Ngày tháng năm sinh', required=True)
    age = fields.Integer(string='Tuổi')
    view_appointment_ids = fields.One2many(comodel_name='dv.appointment', inverse_name='appointment_doctor_id',
                                           string='Số cuộc hẹn')
    total_appointments = fields.Integer(string='Tổng số cuộc hẹn', compute='_get_total_appointments', stored=True)

    def _get_total_appointments(self):
        for record in self:
            record.total_appointments = self.env['dv.appointment'].search_count([('appointment_doctor_id', '=', record.id)])

    def action_state_halftime(self):
        self.state = 'parttime'

    def action_state_fulltime(self):
        self.state = 'fulltime'

    @api.constrains('email')
    def _check_email(self):
        for record in self:
            valid_email = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$',
                                   record.email)
            if valid_email is None:
                raise ValidationError('Vui lòng nhập địa chỉ Email hợp lệ')

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

    @api.model
    def create(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(Doctor, self).create(vals)

    def write(self, vals):
        if vals.get('name', False):
            vals['name'] = vals['name'].title()
        return super(Doctor, self).write(vals)


