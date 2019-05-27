if __name__ == '__main__':
    # from app.models import User, HomeWork, Course, ElectiveCourse, Completion, AdditionalStudentInfo
    # import time
    # print(time.strftime('%Y.%m.%d'))
    # print(Course.query.filter_by(course_name="大学物理").all())
    # print(Course.query.filter_by(course_name="大学物理").first())
    # print(Course.query.get("QQQ111"))

    # student_id = "031602312"
    # course_id = "QQQ111"
    #
    # # ----- course_id的课程需要完成的所有作业
    # homeworks_of_course_all = Course.query.get(course_id).homeworks
    #
    # # ----- 已经上传的作业和未上传作业
    # homeworks_of_course_complete = list()
    # homeworks_of_course_incomplete = list()
    # completions_of_student = Completion.query.filter_by(student_id=student_id).all()
    # homeworks_of_student_complete = list()
    # for completion in completions_of_student:
    #     homeworks_of_student_complete.append(completion.homework)
    # for homework in homeworks_of_course_all:
    #     if homework in homeworks_of_student_complete:
    #         homeworks_of_course_complete.append(homework)
    #     else:
    #         homeworks_of_course_incomplete.append(homework)
    #
    # print(homeworks_of_course_complete)
    # print(homeworks_of_course_incomplete)

    lists = "高等数学第一批作业.JPG"
    for i in range(len(lists)-1, -1, -1):
        if lists[i] == ".":
            break

    print(lists[i:])
    pass
