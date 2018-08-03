from flask import render_template, flash, redirect, request
from app import application
from app import db
from app.forms import AddDomainForm
from app.models import Domain, in_6_months, PhaseEnum
from flask import abort
from app.email import send_verification_email
import hashlib
import jwt
import datetime

@application.route('/')
@application.route('/index')
def index():
    domains = Domain.query.all()
    return render_template('index.html', domains=domains)

@application.route('/add.html', methods=['GET', 'POST'])
def add():
    form = AddDomainForm()
    if form.validate_on_submit():
        domain = Domain(domain=form.domain.data.lower().strip(),
                        email=form.email.data.lower().strip())
        send_verification_email(domain.domain, domain.email)

        db.session.add(domain)
        db.session.commit()

        flash('Domain {} added'.format(
            form.domain.data))

        return redirect('/index')

    return render_template('add.html', form=form)

@application.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error=error)

# yes, I do like to troll people
@application.route('/cron.php', methods=['POST'])
def cron():
    data = request.form
    h = hashlib.sha256()
    h.update(application.config['SECRET_KEY'].encode())
    h.update(b'cron')
    if not "key" in data:
        abort(403)
    if data['key'] != h.hexdigest():
        abort(403)
    return "Ok !!"
    # DO cron stuff

# TODO have a custom 403 to say "token is no longer valid"
@application.route('/verif.php/<key>', methods=['GET'])
def verify_domain(key):
    try:
        domain_to_verify = jwt.decode(key, application.config['SECRET_KEY'], algorithms=['HS256'])
    except jwt.exceptions.DecodeError:
        abort(403)
    do = Domain.query.filter_by(domain=domain_to_verify['domain']).first()
    if do is None:
        abort(404)

    # TODO in 3.7, I would be able to use date.fromisoformat
    (y, m, d) = domain_to_verify['expire'].split('-')
    expiration_date = datetime.date(int(y), int(m), int(d))


    if expiration_date < datetime.date.today(): 
        abort(403)

    do.next_phase = PhaseEnum.sub_domain
    do.next_mail_date = in_6_months()
    do.email = domain_to_verify['email']
    do.first_attempt = True

    db.session.add(do)
    db.session.commit()

    flash('Domain {} verified'.format(do.domain))

    return redirect('/index')



# add a link to reset the countdown
# /reset/domain/secretkey
#  secretkey being sha256
#    domain + date of next renewal + secret key
#    so if the renewal is changed, key no longer valid
#    need to decide the daate before sending the mail (to avoid corner case at midnight)
