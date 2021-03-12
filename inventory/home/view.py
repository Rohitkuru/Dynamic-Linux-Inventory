from flask import Blueprint,render_template,request,flash
from inventory.backend.scripts import scan
from inventory.Crud.operation import add_record


home = Blueprint("home_view",__name__)

@home.route("/",methods = ['GET','POST'])
def home_view():
    if request.method == "POST":
        find_result = scan(request.form['range'])
        if type(find_result) == list:
            flash("Search completed and Inventory updated")
            add_record(find_result,request.form['range'])
            return render_template("home.html",find_result=find_result)
        else:
            flash(find_result)
            return render_template("home.html")
    return render_template("home.html")
