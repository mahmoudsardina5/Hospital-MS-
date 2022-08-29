# -*- coding: utf-8 -*-

from odoo import models, fields, _, api

class CreateAppointment(models.TransientModel):
    _name="create.appointment"

    patient_id = fields.Many2one('hospital.patient', string='Patient')
    appointment_date = fields.Date(string='Appointment Date')

    def create_appointment(self):
        vals = {
            'patient_id': self.patient_id.id,
            'appointment_date': self.appointment_date,
            'notes': 'Created From The Wizard/Code'
        }
        self.env['hospital.appointment'].create(vals)

