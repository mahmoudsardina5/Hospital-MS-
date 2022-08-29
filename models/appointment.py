# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _description = 'Appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = "id desc"

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment') or _('New')
        result = super(HospitalAppointment, self).create(vals)
        return result
    def action_confirm(self):
        for rec in self:
            rec.state='confirm'
    def action_done(self):
        for rec in self:
            rec.state='done'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True,
                       index=True, default=lambda self: _('New'))
    patient_id = fields.Many2one('hospital.patient', string='Patient')
    # patient_name = fields.Char(string='Patient', related='patient_id.patient_name')
    patient_age = fields.Char(string='Age', related='patient_id.patient_age')
    notes = fields.Text(string='Registration Note')
    doctor_note = fields.Text(string='Note')
    appointment_lines = fields.One2many('hospital.appointment.lines', 'appointment_id', string='Appointment Lines')
    pharmacy_note = fields.Text(string='Note')
    appointment_date = fields.Date(string='Date', required=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft')

class HospitalAppointmentLines(models.Model):
    _name = 'hospital.appointment.lines'
    _description = 'Appointment Lines'

    product_id = fields.Many2one('product.product', string='Medicine')
    product_qty = fields.Integer(string='Quantity')
    product_price = fields.Float(string='Price', related='product_id.list_price', readonly=False)
    appointment_id = fields.Many2one('hospital.appointment', string='Appointment ID')

