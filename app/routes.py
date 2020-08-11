from flask import render_template, flash, redirect, request, send_from_directory
from app import application
from app import db
from app.forms import AddDomainForm
from app.models import Domain, in_6_months, PhaseEnum
from app.cron import execute_cron
from flask import abort
from app.email import send_verification_email
import hashlib
import jwt
import datetime

@application.route('/')
@application.route('/index')
def index():
    parent_domains = set()
    domains = Domain.query.all()
    for d in domains:
        p = d.find_parent_domain()
        if p:
            parent_domains.add(p)
        else:
            parent_domains.add(d.domain)

    data = {}
    for p in parent_domains:

        data[p] = {}
        data[p]['email'] = Domain.query.filter(Domain.domain==p).all()[0].email
        data[p]['subdomains'] = []
        for d in domains:
            if d.find_parent_domain() == p:
                data[p]['subdomains'].append({'domain': d.domain, 'email': d.email})

    return render_template('index.html', data=data)

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
    execute_cron()
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

@application.route('/download')
def csv():
    from os import system
    #try:
    system('python /opt/app-root/src/migrations/db2csv.py')
    return send_from_directory('/opt/app-root/src/app/', 'data.csv', as_attachment=True, mimetype='text/csv', attachment_filename=('data.csv'))#send_static_file(f, mimetype = 'text/csv')
    #except OSError:
    #    abort(404)
