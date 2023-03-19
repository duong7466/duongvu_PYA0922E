{
    'name': 'Quản lý phòng khám',
    'version': '1.0',
    'summary': 'Module cho phòng khám',
    'description': """
        Module quản lý phòng khám. Cho phép quản lý thông tin bác sĩ, bệnh nhân,
        lên lịch khám, thực hiện các xét nghiệm y tế ...
        """,
    'author': 'Dương Vũ',
    'depends': [],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/data.xml',

        'views/patient_view.xml',
        'views/doctor_view.xml',
        'views/appointment_view.xml',
        'views/medicaltest_view.xml',

    ],
    'application': True,
    'sequence': 1,
}
