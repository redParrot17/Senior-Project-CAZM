from webscraping.components.student import Student
import mysql.connector


__all__ = ('Database',)


class Database:

    def __init__(self, config_file='mysql.cnf', autocommit=True):
        """ Constructor

        :param config_file: file path of the database configuration file, default 'mysql.cnf'
        :param autocommit:  whether or not to automatically commit changes, default True
        """
        self.db = mysql.connector.connect(option_files=config_file, autocommit=autocommit)

    def close(self):
        self.db.close()

    def select_example(self, argument1, argument2):

        # create a cursor to execute sql statements with
        cursor = self.db.cursor(buffered=True)

        # define the sql statement you want to execute
        sql = "SELECT foo, bar FROM table-name WHERE foo=%s AND bar=%s;"

        # create a tuple of arguments you need to pass
        arg = (argument1, argument2)

        # execute the sql statement
        cursor.execute(sql, arg)

        # fetch all the rows resulting from the sql statement return value
        results = cursor.fetchall()

        # close the cursor
        cursor.close()

        # do something with the results
        return_value = []
        for foo, bar in results:
            return_value.append([foo, bar])
        return return_value

    def getRequirementClasses(self, requirement_id, title):
        cursor = self.db.cursor(buffered=True)
        args = (title, requirement_id)
        sql = """
        SELECT
        COURSE_CODE
        FROM REQUIREMENT INNER JOIN REQUIREMENT_COURSES
        USING(REQUIREMENT_ID)
        WHERE TITLE=%s AND REQUIREMENT_ID=%s;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        courses = []

        for course in results:
            courses.append(course)

        return courses

    def getRequirements(self, major_name, major_year):
        cursor = self.db.cursor(buffered=True)
        args = (major_name, major_year)
        sql = """
        SELECT
        REQUIREMENT_ID, TITLE, REQUIRED_CREDITS, ALTERNATE_REQUIREMENTS
        FROM MAJOR_REQUIREMENTS INNER JOIN REQUIREMENT
        ON REQUIREMENT.REQUIREMENT_ID = MAJOR_REQUIREMENTS.MAJOR_REQUIREMENT_ID
        WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        req_info = {}
        for requirement_id, title, required_credits, alternate_requirements in results:
            req_info[requirement_id] = {
                "alternate_requirements" : alternate_requirements,
                "required_credits" : required_credits,
                "title": title,
                "classes": self.getRequirementClasses(requirement_id, title)
            }

        return req_info

    def search_course_codes(self, argument1):
         cursor = self.db.cursor(buffered=True)
         arg1 = argument1 + "%"
         arg2 = arg1
         args = (arg1,arg2)
         sql = 'SELECT COURSE_CODE, ANY_VALUE(NAME), ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE WHERE COURSE_CODE LIKE %s OR NAME LIKE %s GROUP BY COURSE_CODE;'
         cursor.execute(sql, args)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, name, year, semester in results:
             course_info.append({"course_code":course_code,"name":name,"year": year, "semester": semester})
         return course_info

    def get_all_courses(self):
         cursor = self.db.cursor(buffered=True)
         sql = 'SELECT COURSE_CODE, ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE GROUP BY COURSE_CODE;'
         cursor.execute(sql)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, year, semester in results:
             course_info.append({"courseCode": course_code, "year":year, "semester":semester})
         print(course_info)
         return course_info

    def get_template(self, major_code):
        cursor = self.db.cursor(buffered=True)

        args = (major_code,)
        sql = 'SELECT COURSE_CODE, SEMESTER, YEAR FROM SCHEDULE_COURSES WHERE SCHEDULE_ID=%s ORDER BY YEAR ASC, SEMESTER DESC;'
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        template = []
        courses = []
        current_semester = "FALL"
        current_year = "2020"
        for course_code, semester, year in results:
            if courses and semester + str(year) != current_semester + current_year:
                template.append({'semester': current_semester, 'year':current_year, 'classes': courses}) #append semester schedule to template
                courses = [] #clear courses
                current_semester = semester
                current_year = str(year)
            courses.append(course_code)

        return template


    ### METHODS FOR THE MAJOR TABLE ###


    def does_major_exist(self, major_name: str, major_year: int) -> bool:
        """ Checks whether or not a specific major exists within the database.

        :param major_name: name of the major
        :param major_year: year the major is offered (cannot exceed 2155)
        :return: True if the entry exists, False otherwise
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT 1 FROM MAJOR WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        major_exists = cursor.fetchone() is not None

        cursor.close()
        return major_exists

    def create_new_major(self, major_name: str, major_year: int):
        """ Adds a new major to the database.

        :param major_name: name of the major
        :param major_year: year the major is offered (cannot exceed 2155)
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT IGNORE INTO MAJOR (MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s);'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def delete_old_major(self, major_name: str, major_year: int):
        """ Deletes an existing major from the database.

        :param major_name: name of the major
        :param major_year: year the major is offered (cannot exceed 2155)

        :raises mysql.connector.errors.IntegrityError: if tables MAJOR_REQUIREMENTS or STUDENT_MAJOR depend on this
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM MAJOR WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()


    ### METHODS FOR THE STUDENT MAJOR TABLE ###


    def get_student_majors(self, student_id: int) -> list:
        """ Gets a student's major and year information from the database.

        Example return:

            [('Computer Science', 2017), ('Mathematics', 2017)]

        :param student_id: student's unique identifier
        :return: list of tuples of the major name and year
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT MAJOR_NAME, MAJOR_YEAR FROM STUDENT_MAJOR WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        cursor.execute(sql_query, arguments)
        results = cursor.fetchall()

        cursor.close()
        return results

    def add_major_to_student(self, student_id: int, major_name: str, major_year: int, ensure_major_exists: bool = True):
        """ Adds the specified major information to the database and ignores duplicate entries.

        :param student_id:          student's unique identifier
        :param major_name:          name of the student's major
        :param major_year:          year the student joined the major (cannot exceed 2155)
        :param ensure_major_exists: creates the major if it doesn't exist, default True

        :raises mysql.connector.errors.IntegrityError: if the major does not exist in the major table
        """
        if ensure_major_exists:
            if not self.does_major_exist(major_name, major_year):
                self.create_new_major(major_name, major_year)

        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT INTO STUDENT_MAJOR (STUDENT_ID, MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s, %s) ' \
                    'ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), MAJOR_NAME=VALUES(MAJOR_NAME), ' \
                    'MAJOR_YEAR=VALUES(MAJOR_YEAR);'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def remove_major_from_student(self, student_id: int, major_name: str, major_year: int):
        """ Removes the specified major information from the database for a student.

        :param student_id: student's unique identifier
        :param major_name: name of the student's major
        :param major_year: year the student joined the major (cannot exceed 2155)
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s AND MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def remove_all_majors_from_student(self, student_id: int):
        """ Removes all major information from the database for a student.

        :param student_id: student's unique identifier
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        cursor.execute(sql_query, arguments)
        cursor.close()


    ### METHODS FOR THE STUDENTS TABLE ###


    def get_student(self, student_id: int, adviser_id: int) -> Student:
        """ Retrieves information stored for a student in the database.

        :param student_id: student's unique identifier
        :param adviser_id: adviser's unique identifier
        :return: retrieved student information or None if the student does not exist
        """

        ### Fetch the student's information stored within the STUDENT table ###

        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT STUDENT_ID, ADVISOR_ID, FIRST, LAST, EMAIL, CLASSIFICATION, ' \
                    'GRAD_YEAR, GRAD_SEMESTER, ENROLLED_YEAR, ENROLLED_SEMESTER, ' \
                    'CREDITS_COMPLETED FROM STUDENTS WHERE STUDENT_ID=%s AND ADVISOR_ID=%s;'
        arguments = (student_id, adviser_id,)

        cursor.execute(sql_query, arguments)
        result = cursor.fetchone()

        cursor.close()

        ### Fetch the student's information stored within the STUDENT_MAJOR table ###

        majors = self.get_student_majors(student_id)

        ### Build the Student object containing all the student's data ###

        if result is not None:
            _, advisor_id, firstname, lastname, email, \
                classification, graduation_year, graduation_semester, \
                enrolled_year, enrolled_semester, credits_completed = result

            student = Student(
                student_id=student_id,
                advisor_id=advisor_id,
                firstname=firstname,
                lastname=lastname,
                email=email,
                majors=majors,
                classification=classification,
                graduation_year=graduation_year,
                graduation_semester=graduation_semester,
                enrolled_year=enrolled_year,
                enrolled_semester=enrolled_semester,
                credits_completed=credits_completed)
        else:
            student = None

        return student

    def get_adviser_students(self, adviser_id: int) -> list:
        """ Retrieves all student information associated with an adviser.

        :param adviser_id: adviser's unique identifier
        :return: list of webscraping.components.Student objects associated with the adviser
        """

        ### Retrieve all student ids associated with the adviser id ###

        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT STUDENT_ID FROM STUDENTS WHERE ADVISOR_ID=%s;'
        arguments = (adviser_id,)

        cursor.execute(sql_query, arguments)
        results = cursor.fetchall()
        student_ids = [result[0] for result in results]

        cursor.close()

        ### Retrieve student info for each of the student ids ###

        students = []

        for student_id in student_ids:
            student = self.get_student(student_id, adviser_id)

            if student is not None:
                students.append(student)

        return students

    def create_new_student(self, student: Student, remove_stale_majors: bool = True):
        """ Creates or updates information for a specific student.

        - Ensures the student's major exists when updating major information.
        - Optionally removes stale majors from the student_majors table.

        :param student:             dataclass containing the student's information
        :param remove_stale_majors: removes majors from a student that are not specified
                                    within the student object, default True
        """

        ### Create or update the information stored in the STUDENTS table ###

        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT INTO STUDENTS (STUDENT_ID, ADVISOR_ID, FIRST, LAST, EMAIL, CLASSIFICATION, ' \
                    'GRAD_YEAR, GRAD_SEMESTER, ENROLLED_YEAR, ENROLLED_SEMESTER) VALUES (%s, %s, %s, %s, ' \
                    '%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), ' \
                    'ADVISOR_ID=VALUES(ADVISOR_ID), FIRST=VALUES(FIRST), LAST=VALUES(LAST), EMAIL=VALUES(EMAIL), ' \
                    'CLASSIFICATION=VALUES(CLASSIFICATION), GRAD_YEAR=VALUES(GRAD_YEAR);'
        arguments = (
            student.student_id,
            student.advisor_id,
            student.firstname,
            student.lastname,
            student.email,
            student.classification,
            student.graduation_year,
            student.graduation_semester,
            student.enrolled_year,
            student.enrolled_semester)

        cursor.execute(sql_query, arguments)
        cursor.close()

        ### Create or update the information stored in the STUDENT_MAJOR table ###

        # Determine which majors the student is already registered to
        student_id = student.student_id
        majors_to_add = []
        existing_majors = self.get_student_majors(student_id)

        for major in student.majors:
            if major in existing_majors:
                existing_majors.remove(major)
            else:
                majors_to_add.append(major)

        # Add missing majors to the student
        for major_name, major_year in majors_to_add:
            self.add_major_to_student(student_id, major_name, major_year)

        # Remove extra majors from the student
        if remove_stale_majors:
            for major_name, major_year in existing_majors:
                self.remove_major_from_student(student_id, major_name, major_year)

    def delete_student(self, student_id: int, adviser_id: int,
                       delete_majors=False, delete_schedules=False):
        """ Removes information about a student from the database.

        :param student_id:          student's unique identifier
        :param adviser_id:          adviser's unique identifier

        :param delete_majors:       if the student's major information should
                                    automatically be deleted from the STUDENT_MAJOR
                                    table to avoid a foreign key conflicts, default False

        :param delete_schedules:    if the student's schedules should automatically
                                    be deleted from the SCHEDULE table to avoid a foreign
                                    key conflict, default False

        :raises mysql.connector.errors.IntegrityError:
                if the student still has majors in the STUDENT_MAJOR table or if
                the student has schedules within the SCHEDULE table
        """

        if delete_majors is True:
            self.remove_all_majors_from_student(student_id)

        if delete_schedules is True:
            # TODO: invoke schedule deletion once the method exists
            pass

        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENTS WHERE STUDENT_ID=%s AND ADVISOR_ID=%s;'
        arguments = (student_id, adviser_id,)

        cursor.execute(sql_query, arguments)
        cursor.close()

    def delete_advisers_students(self, adviser_id: int, delete_majors=False, delete_schedules=False):
        """ Removes information for all students associated with an adviser.

        :param adviser_id:          adviser's unique identifier

        :param delete_majors:       if the student's major information should
                                    automatically be deleted from the STUDENT_MAJOR
                                    table to avoid a foreign key conflicts, default False

        :param delete_schedules:    if the student's schedules should automatically
                                    be deleted from the SCHEDULE table to avoid a foreign
                                    key conflict, default False

        :raises mysql.connector.errors.IntegrityError:
                if a student still has majors in the STUDENT_MAJOR table or if
                a student has schedules within the SCHEDULE table
        """

        ### Fetch all student ID's associated with the adviser ###

        cursor = self.db.cursor(buffered=True)

        sql_query = 'SELECT STUDENT_ID FROM STUDENTS WHERE ADVISOR_ID=%s;'
        arguments = (adviser_id,)

        cursor.execute(sql_query, arguments)
        results = cursor.fetchall()
        student_ids = [result[0] for result in results]

        cursor.close()

        ### Perform all of the deletions ###

        for student_id in student_ids:
            self.delete_student(student_id, adviser_id, delete_majors, delete_schedules)
