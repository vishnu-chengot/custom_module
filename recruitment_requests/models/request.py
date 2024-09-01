# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from datetime import datetime, timedelta


class HrRecruitmentRequest(models.Model):
    _name = 'hr.recruitment.request'
    _description = "Recruitment Request"
    _rec_name = 'job_id'

    rr_name = fields.Char('Recruitment Ref',readonly=True)
    name = fields.Text(string="Subject", required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id)
    department_id = fields.Many2one('hr.department', string="Department", required=True)
    job_id = fields.Many2one('hr.job', string="Requested Position")
    job_tmp = fields.Char(string="Job Title")
    employees_count = fields.Integer(string="# of employees", compute='get_employees_count')
    expected_employees = fields.Integer(string="Expected Employees", required=True, default=1)
    date_expected = fields.Date(string="Date Expected", required=True, default=datetime.now().date())
    user_id = fields.Many2one('res.users', string="Requested By", readonly=True, default=lambda self: self.env.user)
    approver_id = fields.Many2one('res.users', string="Approved By", readonly=True)
    refused_by = fields.Many2one('res.users', string="Refused By", readonly=True)
    applicants_count = fields.Integer('# of Application', compute='get_applicants_count')
    reason = fields.Text(string="Remarks")
    description = fields.Text(string="Job Description", required=True)
    requirements = fields.Text(string="Mandatory Skills", required=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('refused', 'Refused'), ('confirmed', 'Waiting Approval'), ('accepted', 'Approved'),
         ('recruiting', 'In recruitment'), ('done', 'Done'),('hold','On Hold'),('cancel','Cancel')], string='State', default='draft')
    applicant_ids = fields.One2many('hr.applicant', 'request_id', string='Applicant', readonly=True)

    employee_ids = fields.One2many('hr.employee', 'request_id', string="Recruited Employees", readonly=True)
    recruited_employees = fields.Integer('Recruited Percentage', compute='get_recruited_employees_percentage')
    existing_job = fields.Selection([('Yes', 'Yes'), ('No', 'No')], string='Existing Job Position', required=True)
    # submit_manager = fields.Many2many('res.users','manager_user_rel','id','user_id', string='Manager')


    @api.onchange('existing_job')
    def update_job(self):
        for res in self:
            res.job_id = False
            res.job_tmp = False

    def get_recruited_employees_percentage(self):
        for percentage in self:
            percentage.recruited_employees = (percentage.employees_count / percentage.expected_employees) * 100

    def get_applicants_count(self):
        for applicants in self:
            applicants.applicants_count = len(applicants.applicant_ids.ids)

    def get_employees_count(self):
        for employee in self:
            employee.employees_count = len(employee.employee_ids.ids)

    @api.model
    def create(self, V):
        seq = self.env['ir.sequence'].next_by_code('hr.recruitment.request') or '/'
        V['rr_name'] = seq
        return super(HrRecruitmentRequest, self).create(V)


    def get_requested_employee_department(self):
        department = False
        if self.env.user in self.env.ref('hr_recruitment.group_hr_recruitment_manager').users:
            department = self.env['hr.department'].search([]).ids
        else:
            department = []
            employee_department = self.env['hr.employee'].search([('user_id','=', self.env.user.id)])
            department.append(employee_department.department_id.id)
            department_object = self.env['hr.department'].search([('manager_id.user_id','=',self.env.user.id)])
            department.append(department_object.id)
        return [('id', 'in', department)]


    @api.onchange('department_id','existing_job')
    def get_requested_position(self):
        position = {}
        if self.department_id:
            job_object = self.env['hr.job'].search([('department_id', '=', self.department_id.id)])
            if job_object:
                position['domain'] = {'job_id': [('id', 'in', job_object.ids)]}
        else:
            position['domain'] = {'job_id': [('id', 'in', [])]}
        return position

    @api.onchange('department_id')
    def update_job_id(self):
        self.job_id = False

    @api.onchange('job_id', 'department_id')
    def get_job_description(self):
        if self.job_id:
            self.description = self.job_id.description
        else:
            self.description = False

    @api.onchange('job_id', 'department_id')
    def get_job_requirements(self):
        if self.job_id:
            self.requirements = self.job_id.requirements
        else:
            self.requirements = False

    def action_confirm(self):
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'submit.recruiting.process',
            'target': 'new',
        }

    #@api.multi
    def action_accept(self):
        approve_template = self.env.ref('recruitment_requests.approve_request_email_template')
        if not self.job_id:
            if approve_template:
                approve_template.sudo().write({'email_to': self.user_id.login})
                self.env['mail.template'].sudo().browse(approve_template.id).send_mail(self.id,
                                                                                       force_send=True)
            return self.write({'state': 'accepted'})

            # return {
            #     'type': 'ir.actions.act_window',
            #     'view_type': 'form',
            #     'view_mode': 'form',
            #     'res_model': 'start.recruiting.process',
            #     'target': 'new',
            # }
        else:
            job_request_object = self.env['hr.job'].search([('id', '=', self.job_id.id)])
            if job_request_object.state == 'open':
                if approve_template:
                    approve_template.sudo().write({'email_to': self.user_id.login})
                    self.env['mail.template'].sudo().browse(approve_template.id).send_mail(self.id,
                                                                          force_send=True)
                return self.write({'state': 'accepted'})
            else:
                # raise ValidationError("An existing request for this job position already in queue")
                raise ValidationError("Job recruitment process in progress related to respective job position.First Complete that one then start a new hiring process.")

    def action_refuse(self):
        self.update({'refused_by': self.env.user.id})
        refuse_template = self.env.ref('recruitment_requests.refuse_request_email_template')
        if refuse_template:
            print("uuu")
            refuse_template.sudo().write({'email_to': self.user_id.login})
            self.env['mail.template'].sudo().browse(refuse_template.id).send_mail(self.id,
                                                                                       force_send=True)
        self.write({
            'state': 'refused'
        })

    def action_draft(self):
        self.write({
            'state': 'draft',
        })

    def action_done(self):
        self.write({
            'state': 'done',
        })

    def name_get(self):
        result = []
        for rec in self:
            if rec.job_id.name:
                print(self.env.context)
                if self.env.context.get('hide_codes'):
                    name = rec.job_id.name
                else:
                    name = '[' + rec.rr_name + '] ' + rec.job_id.name

                result.append((rec.id, name))

            else:
                name = rec.rr_name
                result.append((rec.id, name))
        return result
