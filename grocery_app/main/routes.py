from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import date, datetime
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app.main.forms import GroceryStoreForm, GroceryItemForm

# Import app and db from events_app package so that we can run app
from grocery_app.extensions import app, db

main = Blueprint("main", __name__)

##########################################
#           Routes                       #
##########################################


@main.route("/")
def homepage():
    all_stores = GroceryStore.query.all()
    print(all_stores)
    return render_template("home.html", all_stores=all_stores)


@main.route("/new_store", methods=["GET", "POST"])
@login_required
def new_store():
    form = GroceryStoreForm()
    if form.validate_on_submit():
        new_store = GroceryStore(
            title=form.title.data, address=form.address.data, created_by=current_user
        )
        db.session.add(new_store)
        db.session.commit()
        flash("New store was created successfully.")
        return redirect(url_for("main.store_detail", store_id=new_store.id))
    return render_template("new_store.html", form=form)


@main.route("/new_item", methods=["GET", "POST"])
@login_required
def new_item():
    form = GroceryItemForm()
    if form.validate_on_submit():
        new_item = GroceryItem(
            name=form.name.data,
            price=form.price.data,
            category=form.category.data,
            photo_url=form.photo_url.data,
            store=form.store.data,
            created_by=current_user,
        )
        db.session.add(new_item)
        db.session.commit()
        flash("New Item was created successfully.")
        return redirect(url_for("main.item_detail", item_id=new_item.id))

    return render_template("new_item.html", form=form)


@main.route("/store/<store_id>", methods=["GET", "POST"])
@login_required
def store_detail(store_id):
    store = GroceryStore.query.get(store_id)
    form = GroceryStoreForm(obj=store)
    if form.validate_on_submit():
        store.title = form.title.data
        store.address = form.address.data
        db.session.add(store)
        db.session.commit()
        flash("Store was updated successfully.")
        return redirect(url_for("main.store_detail", store_id=store_id))

    return render_template("store_detail.html", store=store, form=form)


@main.route("/item/<item_id>", methods=["GET", "POST"])
@login_required
def item_detail(item_id):
    item = GroceryItem.query.get(item_id)
    form = GroceryItemForm(obj=item)
    if form.validate_on_submit():
        item.name = form.name.data
        item.price = form.price.data
        item.category = form.category.data
        item.photo_url = form.photo_url.data
        item.store = form.store.data
        db.session.add(item)
        db.session.commit()
        flash("Item was updated successfully.")
        return redirect(url_for("main.item_detail", item_id=item_id))
    return render_template("item_detail.html", item=item, form=form)


@main.route("/add_to_shopping_list/<item_id>", methods=["POST"])
@login_required
def add_to_shopping_list(item_id):
    item = GroceryItem.query.get(item_id)
    current_user.shopping_list_items.append(item)
    db.session.add(current_user)
    db.session.commit()
    shopping_list_items = current_user.shopping_list_items
    return render_template("shoppinglist.html", shopping_list_items=shopping_list_items)


@main.route("/shopping_list")
@login_required
def shopping_list():
    shopping_list_items = current_user.shopping_list_items
    return render_template("shoppinglist.html", shopping_list_items=shopping_list_items)