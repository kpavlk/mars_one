from flask import Flask, render_template
from data import db_session
from data.jobs import Jobs
from data.users import User

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


@app.route('/')
def works_log():
    db_sess = db_session.create_session()
    content = db_sess.query(Jobs).all()

    return render_template('index.html', data=list(content))


if __name__ == '__main__':
    main()
