from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,BooleanField,SubmitField, PasswordField, TextAreaField, RadioField, validators
from wtforms.validators import DataRequired

class formActualizar(FlaskForm):
    titulo = StringField("Titulo",validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"Título"})
    contenido = TextAreaField("Contenido", validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"Contenido del Blog"})
    publico = RadioField('publico', choices = ['Publico', 'Privado'])
    actualizar = SubmitField("Actualizar", render_kw={"onmouseover":"actualizar()"})
    eliminar = SubmitField("Eliminar", render_kw={"onmouseover":"eliminar()"})


class formCrear(FlaskForm):
    titulo = StringField("Título",validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"Título"})
    contenido = TextAreaField("Contenido", validators = [DataRequired(message="No dejar vacío, completar")], render_kw={"placeholder":"Contenido del Blog"})
    publico = RadioField('publico', choices = ['Publico', 'Privado'])
    publicar = SubmitField("Publicar", render_kw={"onmouseover":"publicar()"})
    


class formCambiarContrasena(FlaskForm):    
    claveActual = PasswordField("Contraseña Actual", [validators.DataRequired(message="No dejar vacío, completar")])
    claveNueva = PasswordField('Nueva Contraseña', [validators.DataRequired(message="No dejar vacío, completar"),
                                                   validators.EqualTo('claveNuevaConfirmacion', message='La nueva clave debe coincidir')])
    claveNuevaConfirmacion = PasswordField('Confirmar Contraseña')
    cambiarContrasena = SubmitField("Publicar", render_kw={"onmouseover":"cambiarContrasena()"})