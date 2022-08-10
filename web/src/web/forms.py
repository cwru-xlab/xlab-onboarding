import flask_wtf
import wtforms
from wtforms import widgets


# Ref: https://gist.github.com/ectrimble20/468156763a1389a913089782ab0f272e
class MultiCheckboxField(wtforms.SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class EmailsToDelete(flask_wtf.FlaskForm):
    emails = MultiCheckboxField()
    submit = wtforms.SubmitField("Delete")
