from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField,FloatField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL
from grocery_app.models import ItemCategory, GroceryStore

class GroceryStoreForm(FlaskForm):
    """Form for adding/updating a GroceryStore."""

    title = StringField(
        "Store Title", validators=[DataRequired(), Length(min=3, max=80)]
    )
    address = StringField('Address')
    submit = SubmitField('Submit')
    
    # TODO: Add the following fields to the form class:
    # - title - StringField
    # - address - StringField
    # - submit button
    

class GroceryItemForm(FlaskForm):
    """Form for adding/updating a GroceryItem."""
    name = StringField('item name', 
        validators=[
            DataRequired(), 
            Length(min=3, max=80, message="item name needs to be betweeen 3 and 80 chars")
        ])
    price = FloatField('price')
    category = SelectField('category', choices= ItemCategory.choices())
    photo_url = StringField('photo_url')
    store= QuerySelectField('store',query_factory=lambda: GroceryStore.query )
    submit = SubmitField('submit')
    # TODO: Add the following fields to the form class:
    # - name - StringField
    # - price - FloatField
    # - category - SelectField (specify the 'choices' param)
    # - photo_url - StringField
    # - store - QuerySelectField (specify the `query_factory` param)
    # - submit button
    
