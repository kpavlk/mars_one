from flask import Flask, render_template, redirect
from flask_login import login_user, LoginManager

from data import db_session
from data.jobs import Jobs
from data.users import User
from forms.registerform import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
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
    db_sess.commit()
    app.run(debug=True)
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
    main()
