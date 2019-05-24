if __name__ == '__main__':
    from app import db
    from app.models import *

    db.drop_all()
    db.create_all()

    u1 = User("T031602311", "GZL", "123", "T")
    u2 = User("T031602313", "HCG", "123", "T")
    u3 = User("031602312", "HZB", "123", "S")
    u4 = User("031602316", "HTQ", "123", "S")
    db.session.add_all([u1, u2, u3, u4])

    c1 = Course(id="QQQ111", course_name="高等数学", creator_id="T031602311")
    c2 = Course(id="WWW222", course_name="数据结构", creator_id="T031602311")
    c3 = Course(id="EEE333", course_name="计算机导论", creator_id="T031602313")
    c4 = Course(id="RRR444", course_name="数字逻辑", creator_id="T031602313")
    db.session.add_all([c1, c2, c3, c4])
    db.session.commit()

    cs1 = ElectiveCourse(student_id="031602312", course_id="QQQ111")
    cs2 = ElectiveCourse(student_id="031602312", course_id="EEE333")
    cs3 = ElectiveCourse(student_id="031602316", course_id="WWW222")
    cs4 = ElectiveCourse(student_id="031602316", course_id="RRR444")
    db.session.add_all([cs1, cs2, cs3, cs4])

    h1 = HomeWork(course_id="QQQ111", batch=1, homework_describe="高等数学第一次作业", attach="xxxxx", start_time="2019-1-1",
                  end_time="2019-9-1", upload_num=0, status=True)
    h2 = HomeWork(course_id="WWW222", batch=1, homework_describe="数据结构第一次作业", attach="yyyyy", start_time="2019-4-1",
                  end_time="2019-10-1", upload_num=0, status=True)
    db.session.add_all([h1, h2])

    db.session.commit()

    c1 = Completion(student_id="031602312", homework_id=1, work_name="work_111", complete_time="2019.9.23", score='99',
                    comment='做的非常好', address="2019-05-18_13.22.31.png")
    c2 = Completion(student_id="031602312", homework_id=2, work_name="work_222", complete_time="2019.1.3", score='11',
                    comment='做的非常差', address="2019-05-18_11.11.11.png")
    c3 = Completion(student_id="031602316", homework_id=1, work_name="work_333", complete_time="2019.1.2", score='88',
                    comment='做的好', address="2019-05-18_22.22.22.png")
    c4 = Completion(student_id="031602316", homework_id=2, work_name="work_444", complete_time="2019.1.23", score='99',
                    comment='做的非常好', address="2019-05-18_13.33.33.png")

    db.session.add_all([c1, c2, c3, c4])

    db.session.commit()
