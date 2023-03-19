from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


class Appointment(models.Model):
    _name = 'dv.appointment'
    _description = 'Hospital Appointment'

    name = fields.Char(string='Số tham chiếu', required=True, readonly=True, default=lambda self: ('Lịch khám mới'))
    description = fields.Text(string='Mô tả')
    phone = fields.Char(string='Số điện thoại', related='patient_id.phone')
    email = fields.Char(string='Địa chỉ email', related='patient_id.email')
    dob = fields.Date(string='Ngày tháng năm sinh', related='patient_id.dob')
    age = fields.Integer(string='Tuổi', related='patient_id.age')
    gender = fields.Selection(string='Giới tính',
                              selection=[('male', 'Nam'), ('female', 'Nữ')], related='patient_id.gender')
    state = fields.Selection(string='Trạng thái',
                             selection=[('draft', 'Draft'), ('confirm', 'Confirmed'),
                                        ('done', 'Done'), ('cancel', 'Canceled')], default='draft')
    patient_id = fields.Many2one(comodel_name='dv.patient', string='Bệnh nhân', required=True)
    appointment_date = fields.Datetime(string='Ngày đăng ký khám', default=fields.datetime.now())
    checkup_date = fields.Datetime(string='Khám vào lúc', required=True)
    appointment_doctor_id = fields.Many2one(comodel_name='dv.doctor', string='Tên bác sĩ')
    medical_test_ids = fields.Many2many(comodel_name='dv.medicaltest', relation='medicaltest_appointment_rel',
                                        column1='appointment_id', column2='medicaltest_id', string='Dịch vụ khám')
    prescription_medicine_ids = fields.One2many(comodel_name='dv.appointment.prescription.medicine', inverse_name='appointment_medicine_id'
                                                , string='Toa thuốc')

    @api.constrains('appointment_date', 'checkup_date')
    def _check_date_validation(self):
        for record in self:
            if record.checkup_date < record.appointment_date:
                raise ValidationError('Ngày đặt lịch khám không hợp lệ')


    def action_state_draft(self):
        self.state = 'draft'

    def action_state_confirm(self):
        self.state = 'confirm'

    def action_state_done(self):
        self.state = 'done'

    def action_state_cancel(self):
        self.state = 'cancel'

    @api.model
    def create(self, vals):
        if not vals['description']:
            vals['description'] = "Nhập vào mô tả"
        if vals.get('name', ('Lịch khám mới')) == ('Lịch khám mới'):
            vals['name'] = self.env['ir.sequence'].next_by_code('dv.appointment') or ('Lịch khám mới')

        res = super(Appointment, self).create(vals)
        return res



class Medicine(models.Model):
    _name = 'dv.appointment.prescription.medicine'
    _description = 'Appointment Medicine'

    name = fields.Char(string='Tên thuốc', required=True)
    quantity = fields.Integer(string='Số lượng', default=0)
    appointment_medicine_id = fields.Many2one(comodel_name='dv.appointment', string='Appointment medicine')







