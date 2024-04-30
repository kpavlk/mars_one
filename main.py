from flask import Flask, render_template, redirect, request, abort
from flask_login import login_user, LoginManager, login_required, logout_user, current_user

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.jobsform import JobsForm
from forms.loginform import LoginForm
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def works_log():
    db_sess = db_session.create_session()
    content = db_sess.query(Jobs).all()
    return render_template('index.html', data=list(content))

@app.route('/jobs',  methods=['GET', 'POST'])
@login_required
def add_job():
    form = JobsForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = Jobs()
        jobs.team_leader = form.team_leader.data
        jobs.job = form.job.data
        jobs.work_size = form.work_size.data
        jobs.collaborators = form.collaborators.data
        jobs.is_finished = form.is_finished.data
        db_sess.add(jobs)
        db_sess.commit()
        return redirect('/')
    return render_template('jobs.html', title='Добавление работы',
                           form=form)

@app.route('/jobs/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_jobs(id):
    form = JobsForm()
    if request.method == "GET":
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1)
                                          ).first()
        if jobs:
            form.team_leader.data = jobs.team_leader
            form.job.data = jobs.job
            form.work_size.data = jobs.work_size
            form.collaborators.data = jobs.collaborators
            form.is_finished.data = jobs.is_finished
        else:
            abort(404)
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                          (Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1)
                                          ).first()
        if jobs:
            jobs.team_leader = form.team_leader.data
            jobs.job = form.job.data
            jobs.work_size = form.work_size.data
            jobs.collaborators = form.collaborators.data
            jobs.is_finished = form.is_finished.data
            db_sess.commit()
            return redirect('/')
        else:
            abort(404)
    return render_template('jobs.html',
                           title='Редактирование работы',
                           form=form
                           )

@app.route('/jobs_delete/<int:id>', methods=['GET', 'POST'])
@login_required
def jobs_delete(id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == id,
                                      (Jobs.team_leader == current_user.id) | (Jobs.team_leader == 1)
                                      ).first()
    if jobs:
        db_sess.delete(jobs)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user:
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.hashed_password = user.set_password(form.password.data)
        user.surname = form.surname.data
        user.name = form.name.data
        user.age = int(form.age.data)
        user.position = form.position.data
        user.speciality = form.speciality.data
        user.address = form.address.data

        db_sess.add(user)
        db_sess.commit()

    return render_template('register.html', title='Регистрация', form=form)


if __name__ == '__main__':
    db_session.global_init("db/users.sqlite")
    # user = User(surname="Scott",
    #             name="Ridley",
    #             age=21,
    #             position="captain",
    #             speciality="research engineer",
    #             address="module_1",
    #             email="scott_chief@mars.org"
    #             )
    # user1 = User(surname="Evgeny",
    #             name="Onegin",
    #             age=36,
    #             position="captain",
    #             speciality="copyright manager",
    #             address="module_2",
    #             email="evgeny_onegin@mars.org"
    #             )
    # user2 = User(surname="Elon",
    #             name="Mask",
    #             age=28,
    #             position="director",
    #             speciality="investing manager",
    #             address="module_3",
    #             email="elon_mask@mars.org"
    #             )
    # job = Jobs(team_leader=1,
    #            job="deployment of residential modules 1 and 2",
    #             work_size=15, collaborators="2, 3", is_finished=False)
    db_sess = db_session.create_session()
    # db_sess.add(job)
    # db_sess.commit()
    app.run(debug=True)
