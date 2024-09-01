# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class HrApplicant(models.Model):
    _inherit = 'hr.applicant'

    request_id = fields.Many2one('hr.recruitment.request',string='Job Position',
                                        store=True)
    no_of_position = fields.Integer(string='Number of Position',
                                    related='request_id.expected_employees')
    current_job_state = fields.Selection([
        ('draft', 'Draft'),
        ('recruit', 'Recruitment in Progress'),
        ('done', 'On-Hold'),
        ('open', 'Done'),
        ('cancel', 'Cancel'),
    ], string='Job Status', related='request_id.state', store=True)

    # compute = '_compute_enrollment_request_id',
    # @api.depends('job_id_new')
    # def _compute_enrollment_request_id(self):
    #     for record in self:
    #         record.request_id = record.job_id_new.recruitment_ref


    # @api.depends('job_id')
    # def get_recruitment_request(self):
    #     for rec in self:
    #         print('triggered-----------------')
    #         if rec.job_id:
    #             print('working-----------------')
    #             recruitment_object = self.env['hr.recruitment.request'].search(
    #                 [('job_id', '=', rec.job_id.id)])
    #             for recruitment in recruitment_object:
    #                 rec.request_id = recruitment.id
    #         else:
    #             rec.request_id = False

    def create_employee_from_applicant(self):
        res = super(HrApplicant, self).create_employee_from_applicant()
        res['context'].update({'default_request_id': self.request_id.id or False, })
        return res
