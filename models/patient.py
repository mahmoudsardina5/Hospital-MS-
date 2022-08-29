# -*- coding: utf-8 -*-

from odoo import models, fields, _, api
from odoo.exceptions import ValidationError


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'
    # pat_id = fields.Many2one('hospital.patient')
    patient_name = fields.Char(string='Patient Name')


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _inherits = {'res.partner': 'related_partner_id'}
    _description = 'Patient Record'
    _rec_name = 'name'

    related_partner_id = fields.Many2one('res.partner', string='Related Partner ID')
    # patient_name = fields.Char(string='Name', required=True, track_visibility="always")
    patient_age = fields.Char(string='Age', track_visibility="always")
    notes = fields.Text(string='Notes')
    image = fields.Binary(string='Image')
    appointment_count = fields.Integer(string='Appointment', compute='get_appointment_count')
    name_seq = fields.Char(string='Order Reference', required=True, copy=False, readonly=True,
                           index=True, default=lambda self: _('New'))
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], default='male', string="Gender")
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor')
    ], string="Age Group", compute='set_age_group')

    @api.depends('patient_age')
    def set_age_group(self):
        for rec in self:
            if rec.patient_age:
                if int(rec.patient_age) < 18:
                    rec.age_group = 'minor'
                else:
                    rec.age_group = 'major'

    @api.depends('patient_age')
    @api.onchange('patient_age')
    def check_age(self):
        for rec in self:
            if rec.patient_age:
                if not (rec.patient_age.isdigit()):
                    raise ValidationError(_('error must use number'))

    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('hospital.patient.sequence') or _('New')
        result = super(HospitalPatient, self).create(vals)
        return result
    @api.multi
    def open_patient_appointments(self):
        return {
            'name': _('Appointments'),
            'domain': [('patient_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'hospital.appointment',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
    def get_appointment_count(self):
        count = self.env['hospital.appointment'].search_count([('patient_id', '=', self.id)])
        self.appointment_count = count



    def print(self):
        for rec in self:
            return self.env.ref('om_hospital.patient_card').report_action(self)

    @api.multi
    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s (%s)' % (rec.name_seq, rec.name)))
        return res
