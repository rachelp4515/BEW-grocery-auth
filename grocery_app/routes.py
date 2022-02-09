from importlib.machinery import all_suffixes
from flask import Blueprint, request, render_template, redirect, url_for, flash
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem
from grocery_app.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#               Routes                   #
##########################################

@main.route('/')
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template('home.html', all_stores=all_stores)


#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-/ new STORE

@main.route('/new_store', methods=['GET', 'POST'])
def new_store():
    print(GroceryStore.query.all())

    form = GroceryStoreForm()

    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data,
            address= form.address.data,
        )
        db.session.add(new_store)
        db.session.commit()
        flash('New Store Added')
        return redirect(url_for('main.store_detail', store_id=new_store.id))
    return render_template('new_store.html', form=form)

    # TODO: Create a GroceryStoreForm
    # TODO: If form was submitted and was valid:
    # - create a new GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    # TODO: Send the form to the template and use it to render the form fields


#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-/ new ITEM

@main.route('/new_item', methods=['GET', 'POST'])
def new_item():
    form = GroceryItemForm()

    if form.validate_on_submit():
        new_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
            store = form.store.data
        )
        db.session.add(new_item)
        db.session.commit()

        flash('New Item Added')
        return redirect(url_for('main.item_detail', item_id=new_item.id))
    return render_template('new_item.html', form=form)



#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-/ VIEW / UPDATE store

@main.route('/store/<store_id>', methods=['GET', 'POST'])
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    # TODO: Create a GroceryStoreForm and pass in `obj=store`
    form = GroceryStoreForm(obj=store)
    print("I EXIST HERE")
    if form.validate():
        print("ALOHA")
        update_store = GroceryStore(
            title = form.title.data,
            address = form.address.data,
        )
        # db.session.add(store)
        store.update(update_store)
        print(store)
        # db.session.query(store).update(update_store)
        db.session.commit()

        flash('Store Updated')
        return redirect(url_for('store_detail.html', form = form, store=store))
    # TODO: If form was submitted and was valid:
    # - update the GroceryStore object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the store detail page.

    # TODO: Send the form to the template and use it to render the form fields
    store = GroceryStore.query.get(store_id)
    return render_template('store_detail.html',form=form, store=store)



#_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-_-/ VIEW / UPDATE item

@main.route('/item/<item_id>', methods=['GET', 'POST'])
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    # TODO: Create a GroceryItemForm and pass in `obj=item`
    form = GroceryItemForm(obj = item)

    if form.validate_on_submit():
        update_item = GroceryItem(
            name = form.name.data,
            price = form.price.data,
            category = form.category.data,
            photo_url = form.photo_url.data,
        )
        db.session.add(update_item)
        db.session.commit()

        flash('Item updated')
        return redirect(url_for('item_detail.html', form = form, item = item))
    # TODO: If form was submitted and was valid:
    # - update the GroceryItem object and save it to the database,
    # - flash a success message, and
    # - redirect the user to the item detail page.

    # TODO: Send the form to the template and use it to render the form fields
    item = GroceryItem.query.get(item_id)
    return render_template('item_detail.html', form=form, item=item)

