# -*- coding: utf-8 -*-
from odoo import fields, api, models, _


class StartRecruitingProcess(models.TransientModel):
    _name = 'start.recruiting.process'
    _description = 'Start Recruiting Process'
    recruitment_id = fields.Many2one(
        'hr.recruitment.request',
        default=lambda self: self._default_recruitment(),
        required=True
    )
    hr_responsible = fields.Many2one('res.users', string='Hr Responsible')
    recruitment_responsible = fields.Many2one('res.users', string='Recruitment Responsible')
    recruiter_assign = fields.Many2many('res.users', string='Recruiters Responsible')

    def _default_recruitment(self):
        return self.env['hr.recruitment.request'].browse(self.env.context.get(
            'active_id'))

    def action_start_recruit(self):
        start_recruit_template = self.env.ref('recruitment_requests.start_request_email_template')
        job_stage = self.env['job.stage'].search([
            ('state', '=', 'recruit'),
        ])
        if self.recruitment_id and self.recruitment_responsible:
            self.recruitment_id.recruiter_res = self.recruitment_responsible.id

        if self.recruitment_id and self.recruiter_assign:
            self.recruitment_id.assign_recruiter = [(4,new_customer.id) for new_customer in self.recruiter_assign]
        # recruiter_list = []
        # if self.recruiter_assign:
        #     for recruiter in self.recruiter_assign:



        if self.recruitment_id.job_id:
            reference = self.env['hr.recruitment.request'].search([
                ('rr_name', '=', self.recruitment_id.rr_name),
            ])
            self.recruitment_id.job_id.write({
                'company_id': self.recruitment_responsible.company_id.id,
                'user_id': self.recruitment_responsible.id,
                'hr_responsible_id': self.hr_responsible.id,
                'no_of_recruitment': self.recruitment_id.expected_employees,
                'recruitment_ref': reference.id,
                'location_cmpy': self.recruitment_id.location_cmp,
                'total_year_exp': self.recruitment_id.job_year_exp,
                'hr_recruiter': [(4,new_customer.id) for new_customer in self.recruiter_assign],
                'country_selection': self.recruitment_id.hr_job_country.id,
            })
            self.recruitment_id.write({
                'state': 'recruiting',
                'approver_id': self.env.user.id
            })
            if start_recruit_template:
                if self.recruiter_assign:
                    for i in self.recruiter_assign:
                        dic = {
                            'mail': i.login
                        }
                        dic_mail = dic.values()
                        start_recruit_template.sudo().write({'email_to': ','.join(dic_mail)})
                        self.env['mail.template'].sudo().browse(start_recruit_template.id).send_mail(
                            self.recruitment_id.id, force_send=True)

            return self.recruitment_id.job_id.set_recruit()
        else:
            reference = self.env['hr.recruitment.request'].search([
                ('rr_name', '=',self.recruitment_id.rr_name),
            ])

            new_job_id = self.env['hr.job'].create({'name': self.recruitment_id.job_tmp,
                                                    'company_id': self.recruitment_responsible.company_id.id,
                                                    'department_id': self.recruitment_id.department_id.id,
                                                    'user_id': self.recruitment_responsible.id,
                                                    'description': self.recruitment_id.description,
                                                    'hr_responsible_id': self.hr_responsible.id,
                                                    'no_of_recruitment': self.recruitment_id.expected_employees,
                                                    'requirements': self.recruitment_id.requirements,
                                                    'state': 'recruit',
                                                    'stage_id': job_stage.id,
                                                    'recruitment_ref': reference.id,
                                                    'location_cmpy': self.recruitment_id.location_cmp,
                                                    'total_year_exp': self.recruitment_id.job_year_exp,
                                                    'hr_recruiter': [(4, new_customer.id) for new_customer in self.recruiter_assign],
                                                    'country_selection': self.recruitment_id.hr_job_country.id,
                                                    })
            if start_recruit_template:
                if self.recruiter_assign:
                    for i in self.recruiter_assign:
                        dic = {
                            'mail': i.login
                        }
                        dic_mail = dic.values()
                        start_recruit_template.sudo().write({'email_to': ','.join(dic_mail)})
                        self.env['mail.template'].sudo().browse(start_recruit_template.id).send_mail(
                            self.recruitment_id.id, force_send=True)

            return self.recruitment_id.write({
                'job_id': new_job_id.id,
                'state': 'recruiting',
                'approver_id': self.env.user.id
            })
            # self.recruitment_id.user_id.login