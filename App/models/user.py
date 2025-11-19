from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username =  db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    phone_number = db.Column(db.String(20), nullable=True)

    student = db.relationship('Student', backref='user', uselist=False)
    employer = db.relationship('Employer', backref='user', uselist=False)
    staff = db.relationship('Staff', backref='user', uselist=False)
    
    def __init__(self, username, password, role, email, phone_number=None):
        self.username = username
        self.set_password(password)
        self.role = role
        self.email = email
        self.phone_number = phone_number

    def get_json(self):
        return{
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'email': self.email,
            'phone_number': self.phone_number
        }

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
        

