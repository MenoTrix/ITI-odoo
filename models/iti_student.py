from odoo import models,fields ,api
from odoo.exceptions import UserError, ValidationError



class ItiStudents(models.Model):
    @api.depends("salary")
    def salary_calculate(self):
        for student in self:
           student.tax=student.salary * 0.20
           student.net_salary=student.salary - student.tax
         
    _name="iti.student"
    name=fields.Char()
    email=fields.Char()
    birth_date=fields.Date()
    salary=fields.Float()
    net_salary=fields.Float(compute="salary_calculate")
    tax=fields.Float(compute="salary_calculate", store=True)
    address=fields.Text()
    gender=fields.Selection(
        [('m','Male'),('f',"Female")]
    )
    accepted=fields.Boolean()
    level=fields.Integer()
    image=fields.Binary()
    cv=fields.Html()
    login_time=fields.Datetime()
    state=fields.Selection(
        [
            ('applied','Applied'),
            ('first','First interview'),
            ('second','Second interview'),
            ('passed','Passed'),
            ('rejected','Rejected'),
         
         ],
        default="applied"
    )
    track_id=fields.Many2one("iti.tracks")
    track_capacity=fields.Integer(related="track_id.capacity")
    skill_id=fields.Many2many("iti.skill")
    # accounting_general_ledger=fields.One2many("account.move.line","salary_id")
    
    
    
    @api.onchange('gender')
    def _onchange_gender(self):
        domain={'track_id':[]}
        if self.gender=="m":
            self.salary=10000
            domain={'track_id':[("is_open","=","True")]}
        else: self.salary=5000
        return {
            'domain':domain
        }
    
    def change_state(self):
        if self.state=="applied":
            self.state="first"
        elif self.state=="first":
            self.state="second"
        elif self.state in ["passed","rejected"]:
            self.state="applied"
    
    
    def change_pass(self):
            self.state="passed"
    
    def change_reject(self):
            self.state="rejected"
        
# class StudentSkill(models.Model):
#     _name="iti.student.skill.percentage"
#     student_id=fields.Many2one("iti.student")
#     skill_id=fields.Many2one("iti.skill")
#     grade=fields.Selection([
#         ("g","Good"),("vg","Very Good")
#     ])

    
    @api.model
    def create(self, values):
    # Type of solution #1
        result = super().create(values)
        splited_name=result.name.split()
        result.email=f"{splited_name[0][0]}{splited_name[1]}@gmail.com"
        search_email=self.search([("email","=",values["email"])])
        if search_email==True:
            raise UserError("The Email Already Exist")
        return result
    
    
    _sql_constraints = [
        ("UniqueEmail","UNIQUE(email)","This Email already exist"),
        ("UniqueName","UNIQUE(name)","This Name already exist")
        ]
    
    
    @api.constrains('track_id')
    def _check_track_id(self):
        track_count=len(self.track_id.student_track)
        track_capacity=self.track_id.capacity
        if track_count > track_capacity:
            raise UserError("You Can't Add More Students as the track is full")
            
    
    @api.constrains('salary')
    # Api Constrain enables this condition in create&write function "msh h7tag aktb nfs el condition fel etneen "
    def _check_salary(self):
        if self.salary>10000:
            raise UserError("Salary Can't be over 10000 ")            
    
    def write(self, values):
        # Type of solution #2
        if "name" in values:
            print(values)
            name_split=values["name"].split()
            values["email"]=f"{name_split[0][0]}{name_split[1]}@gmail.com"
        return super().write(values)
    
    

    def unlink(self):  
        # To Delete all Records
        for record in self:
            if record.state  in ["passed","rejected"]:
                raise UserError("You Can't Delete Passed/Rejected Student")
        super().unlink()
        #to delete 1 record
        # if self.state not in ["passed","rejected"]:
        #     super().unlink()
        # else:
        #     raise UserError("You Can't Delete Passed/Rejected Student")
        
    
    # @api.model
    # def create(self, values):
    #     # ***********Another Solution**************
    #     name_split=values["name"].split()
    #     values["email"]=f"{name_split[0][0]}{name_split[1]}@gmail.com"
    #     return super().create(values)
    #     # ******************************************
    #     # result = super().create(values)
    #     # name_split=result.name.split()
    #     # result.email=f"{name_split[0][0]}{name_split[1]}@gmail.com"
    #     # return result
    
    
    
    # @api.multi
    # def write(self, values):
    #     result = super().write(values)
    #     name_split=result.name.split()
    #     result.email=f"{name_split[0][0]}{name_split[1]}@gmail.com"
    #     return result
    