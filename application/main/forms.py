from flask_wtf import FlaskForm
from wtforms import widgets, SelectMultipleField, SubmitField, StringField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

# using function to make a dynamic form
def make_pl_form(my_array):
    class PlaylistForm(FlaskForm):
        files = my_array
        pls = MultiCheckboxField('Playlist', choices=files)  
    return PlaylistForm()

def list_form(my_array):
    class ListForm(FlaskForm):
        files = my_array
        multicheck = MultiCheckboxField(choices=files)  
    return ListForm()