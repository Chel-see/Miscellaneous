from App.database import db
from sqlalchemy.orm import reconstructor

class Application(db.Model):
    __tablename__ = "application"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
    status = db.Column(db.String(15), nullable=False)
    state = None  

    def __init__(self, student_id, position_id):
        self.student_id = student_id
        self.position_id = position_id
        # initial state
        from App.models.applied_state import AppliedState
        self.set_state(AppliedState())

    
     # Rebuild state when loaded from DB
    @reconstructor
    def init_on_load(self):
        self.state = self._state_from_status(self.status)

    @staticmethod   # because states are not stored this helps to load the state based on its last status
    def _state_from_status(status):
        from App.models.applied_state import AppliedState
        from App.models.shortlisted_state import ShortListedState
        from App.models.accepted_state import AcceptedState
        from App.models.rejected_state import RejectedState

        mapping = {
            "Applied": AppliedState(),
            "Shortlisted": ShortListedState(),
            "Accepted": AcceptedState(),
            "Rejected": RejectedState(),
        }
        if status not in mapping:
            raise ValueError(f"Invalid application status: {status}")
        return mapping[status]
        

    # ---------- Delegate to State ----------
    def next(self, decision=None):
        """Move to next state."""
        return self.state.next(self, decision)

    def previous(self):
        return self.state.previous(self)

    def withdraw(self):
        return self.state.withdraw(self)

    # ---------- State setter ----------
    def set_state(self, new_state):
        self.state = new_state
        self.status = new_state.name  # THIS UPDATES THE STATUS
        db.session.add(self)
        db.session.commit()

    def getStatus(self):
        return self.status

    def __repr__(self):
        return f"<Application {self.id} - Status: {self.status}>"































# from App.database import db
# from App.models.context import Context
# from App.models.applied_state import AppliedState
# from App.models.shortlisted_state import ShortListedState
# from App.models.rejected_state import RejectedState

# class Application(db.Model):
#     __tablename__ = "application"

#     id = db.Column(db.Integer, primary_key=True)
#     student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
#     position_id = db.Column(db.Integer, db.ForeignKey('position.id'), nullable=False)
#     status = db.Column(db.String(15), default="applied", nullable=False)
#     type = db.Column(db.String(50))

#     def __init__(self, student_id, position_id):
#         self.student_id = student_id
#         self.position_id = position_id
#         self.context = Context(AppliedState())
#         self.status = self.context.state.name #applied

#     def getStatus(self):
#         return self.status

#     def setStatus(self, newStatus:str): # transition to shortlisted / accepted / rejected states
#         if isinstance(self.context.state, AppliedState) and newStatus=="shortlisted": #Applied -> Shortlisted
#             self.context.setState(ShortListedState())
#         elif isinstance(self.context.state, ShortListedState): #Shortlisted -> Accepted / Rejected
#             self.context.state.next_decision(newStatus)
#         elif isinstance(self.context.state, ShortListedState()) and newStatus=="applied":
#             self.context.state.previous()
#         elif isinstance(self.context.state, RejectedState()) and newStatus=="shortlisted":
#             self.context.state.previous()
#         elif newStatus == "withdrawn": #Student withdraws from position
#             self.context.setState(RejectedState())
#         self.status = self.context.state.name
#         db.session.commit()

#     def __repr__(self):
#         return f'<Application id: {self.id} - Student ID: {self.student_id} - Position ID: {self.position_id} - Status: {self.status}>'

