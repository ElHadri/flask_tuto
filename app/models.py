# database models

from app import db


# Models------------------------------------------------------------------
class Role(db.Model):
   __tablename__ = 'roles'
   id = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(64), unique=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<Role %r>' % self.name
   
   # lazy='dynamic': to request that the query is not automatically executed. To return a query object not a list
   users = db.relationship('User', backref='role', uselist=True, lazy='dynamic')  # represents the object-oriented view of the relationship.

class User(db.Model):
   __tablename__ = 'users'
   id = db.Column(db.Integer, primary_key=True)
   username = db.Column(db.String(64), unique=True, index=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<User %r>' % self.username

   role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

   # role (hidden attribute - object-oriented view ) !!

class Modele(db.Model):
   __tablename__ = 'Modeles'
   id = db.Column(db.Integer, primary_key=True)
   label = db.Column(db.String(64), unique=True)
   
   def __repr__(self):  # give model a readable string representation that can be used for debugging and testing purposes.
      return '<Modele %r>' % self.label

# -------------------------------------------------------------------------
