from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class AddSateliteForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    pos = StringField('Position [km]', validators=[DataRequired()])
    vel = StringField('Velocity [km/s]', validators=[DataRequired()])
    submit = SubmitField('Add Satelite')

    def validate_pos(self, pos):
        try:
            pos_list = (pos.data).replace(' ', '').split(',')
            pos_list = [int(x) for x in pos_list]
        except:
            raise ValidationError('Position has to be in the format: "x, y, z" ,where values are numbers. Example: 10000, 0, 0')
        if len(pos_list) != 3:
            raise ValidationError('Position vector has to have 3 elements')

    def validate_vel(self, vel):
        try:
            vel_list = (vel.data).replace(' ', '').split(',')
            vel_list = [int(x) for x in vel_list]
        except:
            raise ValidationError('Velocity has to be in the format: "v_x, v_y, v_z" ,where values are numbers. Example: 0, 7.0, 0')
        if len(vel_list) != 3:
            raise ValidationError('Velocity vector has to have 3 elements')