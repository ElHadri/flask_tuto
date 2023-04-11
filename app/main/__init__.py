# main package constructor
# main (first) blueprint creation (global scope)
from flask import Blueprint
main = Blueprint('main', __name__) # takes two required arguments: the blueprint name and the module or package where the blueprint is located.
from . import views, errors #  these modules are imported at the bottom of this script to avoid errors due to circular dependencies. (because in turn import the main blueprint object)