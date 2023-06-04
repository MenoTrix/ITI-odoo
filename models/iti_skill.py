from odoo import fields,models


class StudentSkill(models.Model):
    _name="iti.skill"
    name=fields.Char()
    student_skill=fields.Many2many("iti.student")