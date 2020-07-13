# no auto, need 3.6
from enum import Enum
from app import db
import datetime

# hardcoded to be 6 months
def in_6_months():
    return datetime.date.today()  + datetime.timedelta(weeks=26)

def in_1_week():
    return datetime.date.today()  + datetime.timedelta(weeks=1)

class PhaseEnum(Enum):
    # when we match a subdomain
    sub_domain = 1
    # when subdomain get no answer
    root_domain = 2
    # when no one answer
    manager = 3
    # before first verification
    need_verification = 4

class Domain(db.Model):
    domain = db.Column(db.String(64), index=True, unique=True, primary_key=True)
    email = db.Column(db.String(120), index=True, unique=False)
    next_phase = db.Column(db.Enum(PhaseEnum), default=PhaseEnum.need_verification)
    next_mail_date = db.Column(db.Date(), default=in_6_months())
    first_attempt = db.Column(db.Boolean(), default=True)

    def find_parent_domain(self):
        d = self.domain.lower().split('.')
        while len(d) != 1:
            d = d[1:]
            r = Domain.query.filter_by(domain='.'.join(d)).first()
            if r is not None:
                return r.domain
        return None

