if __name__ == '__main__':
    from app import db
    from app.models import *

    db.drop_all()
    db.create_all()

    u1 = User("T031602311", "郭子龙", "123", "T")
    u2 = User("T031602319", "雷光游", "123", "T")
    u3 = User("031602324", "林集", "123", "S")
    u4 = User("031602335", "吴宜钊", "123", "S")
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    # c1 = Course(id="QQQ111", course_name="高等数学", creator_id="T031602311")
    # c2 = Course(id="WWW222", course_name="数据结构", creator_id="T031602311")
    # c3 = Course(id="EEE333", course_name="计算机导论", creator_id="T031602319")
    # c4 = Course(id="RRR444", course_name="数字逻辑", creator_id="T031602319")
    # db.session.add_all([c1, c2, c3, c4])
    # db.session.commit()
    #
    # cs1 = ElectiveCourse(student_id="031602324", course_id="QQQ111")
    # cs2 = ElectiveCourse(student_id="031602324", course_id="WWW222")
    # cs3 = ElectiveCourse(student_id="031602324", course_id="EEE333")
    # cs4 = ElectiveCourse(student_id="031602324", course_id="RRR444")
    # cs5 = ElectiveCourse(student_id="031602335", course_id="QQQ111")
    # cs6 = ElectiveCourse(student_id="031602335", course_id="WWW222")
    # cs7 = ElectiveCourse(student_id="031602335", course_id="EEE333")
    # cs8 = ElectiveCourse(student_id="031602335", course_id="RRR444")
    # db.session.add_all([cs1, cs2, cs3, cs4, cs5, cs6, cs7, cs8])
    # db.session.commit()


    # h1 = HomeWork(course_id="QQQ111", batch=1, homework_describe="高等数学第一次作业", attach=None, start_time="2019-1-1",
    #               end_time="2019-9-1", upload_num=2, status="进行中")
    # h2 = HomeWork(course_id="WWW222", batch=1, homework_describe="数据结构第一次作业", attach=None, start_time="2019-4-1",
    #               end_time="2019-10-1", upload_num=2, status="进行中")
    # db.session.add_all([h1, h2])
    # db.session.commit()
    #
    # c1 = Completion(student_id="031602324", homework_id=1, complete_time="2019-1-3", score='99',
    #                 comment='做的非常好！', address="031602324_1.png")
    # c2 = Completion(student_id="031602324", homework_id=2, complete_time="2019-5-1", score='11',
    #                 comment='做的非常差，上课认真听讲！', address="031602324_1.png")
    # c3 = Completion(student_id="031602335", homework_id=1, complete_time="2019-2-3", score='60',
    #                 comment='继续努力。', address="031602335_1.png")
    # c4 = Completion(student_id="031602335", homework_id=2, complete_time="2019-4-13", score='99',
    #                 comment='做的很好，继续加油！', address="031602335_2.png")
    #
    # db.session.add_all([c1, c2, c3, c4])
    # db.session.commit()

    # a1 = AdditionalStudentInfo("031602324", "2016", "福州大学", "数学与计算机科学学院", "网络工程", "1999-1-1")
    # a2 = AdditionalStudentInfo("031602335", "2016", "福州大学", "数学与计算机科学学院", "计算机科学与技术", "1998-1-1")
    # db.session.add_all([a1, a2])
    # db.session.commit()
