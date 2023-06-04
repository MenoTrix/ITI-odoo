from odoo import fields,models

class ItiTracks(models.Model):
    _name="iti.tracks"
    name=fields.Char()
    is_open=fields.Boolean()
    capacity=fields.Integer()
    student_track=fields.One2many("iti.student","track_id")
    