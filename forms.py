from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    remember = BooleanField('Recordar sesión')
    submit = SubmitField('Iniciar Sesión')

class RegistrationForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[
        DataRequired(),
        Length(min=4, max=50)
    ])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirmar Contraseña', 
                                   validators=[DataRequired(), EqualTo('password')])
    role = RadioField('Tipo de cuenta', choices=[
        ('cliente', 'Cliente'),
        ('admin', 'Administrador')
    ], default='cliente')
    admin_key = PasswordField('Clave de administrador')
    
    submit = SubmitField('Registrarse')

    def validate_admin_key(self, field):
        if self.role.data == 'admin' and field.data != '22':
            raise ValidationError('Clave de administrador incorrecta')