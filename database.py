from webscraping.components.student import Student
from webscraping.components.schedule import Schedule
from webscraping.components.course import Course
from webscraping.errors import StudentDoesntExist
import mysql.connector
from datetime import date


__all__ = ('Database',)


class Database:

    def __init__(self, config_file='mysql.cnf', autocommit=True):
        """ Constructor

        :param config_file: file path of the database configuration file, default 'mysql.cnf'
        :param autocommit:  whether or not to automatically commit changes, default True
        """
        self.autocommit = autocommit
        self.db = mysql.connector.connect(option_files=config_file, autocommit=False)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.db.close()

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


    '''
    EXAMPLE JSON:

    {
        "COURSE CODE": {
            REQUIREMENT_TYPE: {
                REQUIREMENT_GROUP: [REQUISITE CODE, REQUISITE CODE],
                REQUIREMENT_GROUP: [REQUISITE CODE, REQUISITE CODE, REQUISITE CODE]
            }
    }

    }

    '''
    def getRequisites(self):
        cursor = self.db.cursor(buffered=True)

        sql = """
        SELECT COURSE_CODE, REQUISITE_CODE, TYPE, REQUISITE_GROUP FROM REQUISITES
            """
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        courses = {}

        for course_code, requisite_code, type, group in results:
            if course_code not in courses:
                #Make new K/V Pair course_code
                courses[course_code] =  {type : {group: [requisite_code]}}
            else:

                if type in courses[course_code]:
                    if group in courses[course_code][type]:
                        courses[course_code][type][group].append(requisite_code)
                    else:
                        courses[course_code][type][group] = [requisite_code]
                else:
                    courses[course_code][type] = {group: [requisite_code]}
        return courses


    def get_alternates_by_cluster(self, cluster_id):
        cursor = self.db.cursor(buffered=True)

        args = (cluster_id,)
        sql = '''
        select ALT_CLUSTER from ALT_CLUSTERS where CLUSTER_ID  = %s;
        '''
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code in results:
            course_info.append(course_code)
        return course_info

    def get_courses_by_cluster(self, cluster_id):
        cursor = self.db.cursor(buffered=True)
        args = (cluster_id,)
        sql = """
            Select COURSE_CODE from CLUSTER_COURSES where CLUSTER_ID = %s ;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        cluster=[]
        for course_code in results:
            cluster.append(course_code)
        return cluster

    def get_clusters_by_requirement(self, requirement_id):

        cursor = self.db.cursor(buffered=True)
        args = (requirement_id,)
        sql = """
       SELECT CLUSTER_ID, REQUIRED_CREDITS from CLUSTERS where REQUIREMENT_ID = %s;
            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

         
        group = {}
        for cluster_id, required_credits in results:
            courses = self.get_courses_by_cluster(cluster_id)
            group[cluster_id] = {
                "courses" : courses,
                "credits" : required_credits,
                "alternate_clusters": self.get_alternates_by_cluster(cluster_id)
            }
        
            
        return group


    def getRequirements(self, major_name, major_year):
        cursor = self.db.cursor(buffered=True)
        args = (major_name, major_year,)
        sql = """
        SELECT  TITLE,  REQUIREMENT_ID , SPECIAL
        FROM MAJOR_REQUIREMENTS INNER JOIN REQUIREMENT
        ON REQUIREMENT.REQUIREMENT_ID = MAJOR_REQUIREMENTS.MAJOR_REQUIREMENT_ID
        WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s

            """
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        req_info = {}
        for title, requirement_id, special in results:
            req_info[requirement_id] = {
                
                "title": title,
                "clusters": self.get_clusters_by_requirement(requirement_id),
                "special": special

            }

        return req_info


    def search_course_codes(self, argument1):
        cursor = self.db.cursor(buffered=True)
        arg1 = argument1 + "%"
        arg2 = arg1
        args = (arg1,arg2,)
        sql = 'SELECT COURSE_CODE, ANY_VALUE(NAME), ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE WHERE COURSE_CODE LIKE %s OR NAME LIKE %s GROUP BY COURSE_CODE;'
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, name, year, semester in results:
            course_info.append({"course_code":course_code,"name":name,"year": year, "semester": semester})
        return course_info

    def filter_duplicates(self, schedule_id):
        cursor = self.db.cursor(buffered=True)
        currentYear = date.today().year
        args = (schedule_id, currentYear,)
        sql = 'SELECT COURSE_CODE, ANY_VALUE(NAME), ANY_VALUE(YEAR), ANY_VALUE(SEMESTER) FROM COURSE WHERE COURSE_CODE NOT IN (SELECT COURSE_CODE FROM SCHEDULE_COURSES WHERE SCHEDULE_ID=%s AND YEAR<=%s) GROUP BY COURSE_CODE;'
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, name, year, semester in results:
            course_info.append({"course_code":course_code,"name":name,"year": year, "semester": semester})
        return course_info

    def get_all_courses(self):
        cursor = self.db.cursor(buffered=True)
        sql = 'SELECT COURSE_CODE, ANY_VALUE(YEAR), ANY_VALUE(SEMESTER), ANY_VALUE(CREDITS) FROM COURSE GROUP BY COURSE_CODE;'
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, year, semester, credits in results:
            course_info.append({"courseCode": course_code, "year":year, "semester":semester, "credits": credits})
        return course_info

    def get_courses_by_year_and_semester(self, semester, year):
        cursor = self.db.cursor(buffered=True)
        sql = 'SELECT COURSE_CODE, YEAR, SEMESTER, CREDITS FROM COURSE WHERE Year LIKE ? AND SEMESTER LIKE ?;'
        cursor.execute(sql, (year, semester))
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, year, semester, credits in results:
            course_info.append({"courseCode": course_code, "year":year, "semester":semester, "credits": credits})
        return course_info

    def get_courses(self):
        cursor = self.db.cursor(buffered=True)
        sql = 'SELECT COURSE_CODE, YEAR, SEMESTER, CREDITS FROM COURSE;'
        cursor.execute(sql)
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, year, semester, credits in results:
            course_info.append({"courseCode": course_code, "year":year, "semester":semester, "credits": credits})
        return course_info

    def get_template(self, major_code):
        cursor = self.db.cursor(buffered=True)

        args = (major_code,)
        sql = 'SELECT COURSE_CODE, SEMESTER, YEAR FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s ORDER BY YEAR ASC, SEMESTER DESC;'
        cursor.execute(sql, args)
        results = cursor.fetchall()
        cursor.close()

        template = []
        courses = []
        current_semester = "Spring"
        current_year = "2021"
        for course_code, semester, year in results:
            if courses and semester + str(year) != current_semester + current_year:
                template.append({'semester': current_semester, 'year':current_year, 'classes': courses}) #append semester schedule to template
                courses = [] #clear courses
                current_semester = semester
                current_year = str(year)
            courses.append(course_code)

        return template


    ### METHODS FOR THE COURSE TABLE ###


    def get_course(self, course_code: str, year: int, semester: str) -> Course:
        """ Retrieves information stored for a course in the database.

        :param course_code: course's unique identifier
        :param year:        year the course is offered
        :param semester:    semester the course is offered
        :return: retrieved course info or None if the course does not exist
        """

        course = None
        cursor = self.db.cursor(buffered=True)

        # Prepare the SQL query
        sql_query = 'SELECT CREDITS, NAME FROM COURSE WHERE COURSE_CODE=%s AND SEMESTER=%s;'
        arguments = (course_code, semester,)

        # Execute the SQL query
        cursor.execute(sql_query, arguments)
        result = cursor.fetchone()

        # Parse the result into a course object
        if result is not None:
            credit_hours, name = result
            course = Course(
                course_code=course_code,
                name=name,
                credit_hours=credit_hours,
                year=year,
                semester=semester)

        cursor.close()
        return course

    def search_courses(self, search_query: str, ignore_semester=False) -> list:
        """ Searches for courses who's codes or names match a search query.

        This supports partial matching and will strip any '%'
        character from the front and back of the search query.

        :param search_query:    string to match against course identifiers

        :param ignore_semester: if duplicate courses from different semesters should be ignored,
                                if ignored then year and semester will be None, default False

        :return: list of Course objects that match the search query
        """

        # Prepare search_query for partial matching.
        search_query = search_query.strip('%')
        search_query = f'%{search_query}%'
        search_results = []

        # Buffered so that we fetch all results to prevent other DB calls
        # on the same connection from crashing due to incomplete cleanup.
        cursor = self.db.cursor(buffered=True)

        if ignore_semester:

            # Build the SQL query
            sql_query = 'SELECT COURSE_CODE, ANY_VALUE(CREDITS), ANY_VALUE(NAME) FROM COURSE ' \
                        'WHERE COURSE_CODE LIKE %s OR NAME LIKE %s GROUP BY COURSE_CODE;'
            arguments = (search_query, search_query,)

            # Execute the SQL query
            cursor.execute(sql_query, arguments)
            results = cursor.fetchall()

            # Parse the results into course objects
            for course_code, credit_hours, name in results:
                course = Course(
                    course_code=course_code,
                    name=name,
                    credit_hours=credit_hours,
                    year=None,
                    semester=None)
                search_results.append(course)

        else:

            # Build the SQL query
            sql_query = 'SELECT COURSE_CODE, CREDITS, NAME, SEMESTER, YEAR FROM ' \
                        'COURSE WHERE COURSE_CODE LIKE %s OR NAME LIKE %s;'
            arguments = (search_query, search_query,)

            # Execute the SQL query
            cursor.execute(sql_query, arguments)
            results = cursor.fetchall()

            # Parse the results into course objects
            for course_code, credit_hours, name, semester, year in results:
                course = Course(
                    course_code=course_code,
                    name=name,
                    credit_hours=credit_hours,
                    year=year,
                    semester=semester)
                search_results.append(course)

        cursor.close()
        return search_results

    def get_course_objects_by_semester_and_year(self, semester: str, year: int) -> list:
        """ Retrieves courses associated with a semester and year.

        :param semester:    semester the course is offered
        :param year:        year the course is offered
        :return: list of Course objects satisfying the arguments
        """

        # Buffered so that we fetch all results to prevent other DB calls
        # on the same connection from crashing due to incomplete cleanup.
        cursor = self.db.cursor(buffered=True)

        # Build the SQL query
        sql_query = 'SELECT COURSE_CODE, CREDITS, NAME FROM COURSE WHERE SEMESTER=%s AND YEAR=%s;'
        arguments = (semester, year,)

        # Execute the SQL query
        cursor.execute(sql_query, arguments)
        results = cursor.fetchall()

        cursor.close()

        # Parse the results into course objects
        search_results = []
        for course_code, credit_hours, name in results:
            course = Course(
                course_code=course_code,
                name=name,
                credit_hours=credit_hours,
                year=year,
                semester=semester)
            search_results.append(course)

        return search_results

    def get_courses_by_semester(self, semester):
        cursor = self.db.cursor(buffered=True)
        sql = 'SELECT COURSE_CODE, YEAR, SEMESTER, CREDITS FROM COURSE WHERE SEMESTER LIKE %s;'
        cursor.execute(sql, (semester,))
        results = cursor.fetchall()
        cursor.close()

        course_info = []
        for course_code, year, semester, credits in results:
            course_info.append({"courseCode": course_code, "year":year, "semester":semester, "credits": credits})
        return course_info


    ### METHODS FOR SCHEDULE RELATED TABLES ###


    def does_schedule_exist(self, student_id: int) -> bool:
        """ Checks if a student has a schedule in the database.

        :param student_id: student's unique identifier
        :return: True if a schedule exists for the student, False otherwise
        """

        cursor = self.db.cursor(buffered=True)

        # Prepare the SQL query
        sql_query = 'SELECT 1 FROM SCHEDULE WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        # Execute the SQL query
        cursor.execute(sql_query, arguments)
        result = cursor.fetchone()

        cursor.close()
        return result is not None

    def get_student_schedule(self, student_id: int) -> Schedule:
        """ Retrieves information stored for a student's schedule in the database.

        :param student_id: student's unique identifier
        :return: retrieved schedule info or None if the schedule does not exist
        """

        # Buffered so that we fetch all results to prevent other DB calls
        # on the same connection from crashing due to incomplete cleanup.
        cursor = self.db.cursor(buffered=True)
        course_identifiers = []
        schedule = None

        ### Fetch the schedule status ###

        # Prepare the SQL query
        sql_query = 'SELECT SCHEDULE_STATUS FROM STUDENTS WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        # Execute the SQL query
        cursor.execute(sql_query, arguments)
        result = cursor.fetchone()

        # Parse the result into a schedule object
        if result is not None and result[0] != 0:
            schedule = Schedule(student_id=student_id, status=result[0], courses=[])

            ### Fetch the schedule's course identifiers ###

            # Prepare the SQL query
            sql_query = 'SELECT COURSE_CODE, YEAR, SEMESTER FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s;'
            arguments = (student_id,)

            # Execute the SQL query
            cursor.execute(sql_query, arguments)
            course_identifiers = cursor.fetchall()

        cursor.close()

        ### Fetch the course information for each course identifier ###
        print("HERE!!!!!!!!!!!!!!",course_identifiers)
        if schedule is not None:
            for course_code, year, semester in course_identifiers:
                course = self.get_course(course_code, year, semester)
                if course is not None:
                    print("GETTING HERE", course)
                    schedule.courses.append(course)

        return schedule


    def clearStudentSchedule(self, student_id:int):
        cursor = self.db.cursor(buffered=True)
        sql_query = 'DELETE FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s;'
        arguments = (student_id,)
        cursor.execute(sql_query, arguments)
        cursor.close()
        # commit the changes to the database
        self.db.commit()

    def addCourseToStudentSchedule(self, student_id, course_code, semester, year):
        cursor = self.db.cursor(buffered=True)
        sql_query = 'INSERT INTO SCHEDULE_COURSES (STUDENT_ID, COURSE_CODE, YEAR, SEMESTER) VALUES (%s, %s, %s, %s);'
        arguments = (student_id, course_code, year, semester)
        cursor.execute(sql_query, arguments)
        cursor.close()
        # commit the changes to the database
        self.db.commit()

    def setStudentStatus(self, student_id, status):
        cursor = self.db.cursor(buffered=True)
        sql_query = 'UPDATE STUDENTS SET SCHEDULE_STATUS = %s WHERE STUDENT_ID =%s;'
        arguments = (status, student_id)
        cursor.execute(sql_query, arguments)
        cursor.close()
        # commit the changes to the database
        self.db.commit()

    def update_student_schedule(self, schedule: Schedule, remove_stale_courses=True, *, suppress_commit=False):
        """ Creates or updates a student's schedule in the database.

        :param schedule:                schedule containing the changes to be implemented
        :param remove_stale_courses:    if courses not included in schedule should be removed
        :param suppress_commit:         if autocommit should be suppressed, default False

        :raises webscraping.errors.StudentDoesntExist: if no student exists with a matching student id
        """

        # Buffered so that we fetch all results to prevent other DB calls
        # on the same connection from crashing due to incomplete cleanup.
        cursor = self.db.cursor(buffered=True)
        student_id = schedule.student_id

        ### Ensure student actually exists ###

        sql_query = 'SELECT 1 FROM STUDENTS WHERE STUDENT_ID=%s;'
        arguments = (student_id,)
        cursor.execute(sql_query, arguments)
        student_exists = cursor.fetchone() is not None

        if not student_exists:
            raise StudentDoesntExist(f"Cannot update the schedule of student {student_id} because they don't exist.")

        ### Update the schedule status ###

        sql_query = 'UPDATE STUDENTS SET SCHEDULE_STATUS=%s WHERE STUDENT_ID=%s;'
        arguments = (schedule.status, student_id,)
        cursor.execute(sql_query, arguments)

        ### Determine which courses already exist for this schedule ###

        sql_query = 'SELECT COURSE_CODE, YEAR, SEMESTER FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s;'
        arguments = (student_id,)
        cursor.execute(sql_query, arguments)

        courses_in_database = set(
            (student_id, course_code, year, semester,)
            for course_code, year, semester in cursor.fetchall())

        courses_in_schedule = set(
            (student_id, course.course_code, course.year, course.semester,)
            for course in schedule.courses)

        courses_to_add = courses_in_schedule - courses_in_database
        courses_to_del = courses_in_database - courses_in_schedule

        ### Remove stale courses if applicable ###

        if remove_stale_courses:

            sql_query = 'DELETE FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s ' \
                        'AND COURSE_CODE=%s AND YEAR=%s AND SEMESTER=%s;'
            cursor.executemany(sql_query, list(courses_to_del))

        ### Add the fresh courses ###

        sql_query = 'INSERT INTO SCHEDULE_COURSES (STUDENT_ID, COURSE_CODE, YEAR, SEMESTER) ' \
                    'VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), ' \
                    'COURSE_CODE=VALUES(COURSE_CODE), YEAR=VALUES(YEAR), SEMESTER=VALUES(SEMESTER);'
        cursor.executemany(sql_query, list(courses_to_add))

        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def delete_student_schedule(self, student_id: int, *, suppress_commit=False):
        """ Deletes a student's schedule from the database.

        :param student_id:      student's unique identifier
        :param suppress_commit: if autocommit should be suppressed, default False
        """

        cursor = self.db.cursor(buffered=True)

        ### Delete all the courses from the schedule ###

        sql_query = 'DELETE FROM SCHEDULE_COURSES WHERE STUDENT_ID=%s;'
        arguments = (student_id,)
        cursor.execute(sql_query, arguments)

        ### Delete base schedule from the database ###

        sql_query = 'UPDATE STUDENTS SET SCHEDULE_STATUS=%s WHERE STUDENT_ID=%s;'
        arguments = (0, student_id,)
        cursor.execute(sql_query, arguments)

        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()


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

    def create_new_major(self, major_name: str, major_year: int, *, suppress_commit=False):
        """ Adds a new major to the database.

        :param major_name:      name of the major
        :param major_year:      year the major is offered (cannot exceed 2155)
        :param suppress_commit: if autocommit should be suppressed, default False
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT IGNORE INTO MAJOR (MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s);'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def delete_old_major(self, major_name: str, major_year: int, *, suppress_commit=False):
        """ Deletes an existing major from the database.

        :param major_name:      name of the major
        :param major_year:      year the major is offered (cannot exceed 2155)
        :param suppress_commit: if autocommit should be suppressed, default False

        :raises mysql.connector.errors.IntegrityError: if tables MAJOR_REQUIREMENTS or STUDENT_MAJOR depend on this
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM MAJOR WHERE MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()


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

    def add_major_to_student(self, student_id: int, major_name: str,
                             major_year: int, ensure_major_exists=True,
                             *, suppress_commit=False):
        """ Adds the specified major information to the database and ignores duplicate entries.

        :param student_id:          student's unique identifier
        :param major_name:          name of the student's major
        :param major_year:          year the student joined the major (cannot exceed 2155)
        :param ensure_major_exists: creates the major if it doesn't exist, default True
        :param suppress_commit:     if autocommit should be suppressed, default False

        :raises mysql.connector.errors.IntegrityError: if the major does not exist in the major table
        """

        if ensure_major_exists:
            if not self.does_major_exist(major_name, major_year):
                self.create_new_major(major_name, major_year, suppress_commit=True)

        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT INTO STUDENT_MAJOR (STUDENT_ID, MAJOR_NAME, MAJOR_YEAR) VALUES (%s, %s, %s) ' \
                    'ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), MAJOR_NAME=VALUES(MAJOR_NAME), ' \
                    'MAJOR_YEAR=VALUES(MAJOR_YEAR);'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def remove_major_from_student(self, student_id: int, major_name: str, major_year: int, *, suppress_commit=False):
        """ Removes the specified major information from the database for a student.

        :param student_id:      student's unique identifier
        :param major_name:      name of the student's major
        :param major_year:      year the student joined the major (cannot exceed 2155)
        :param suppress_commit: if autocommit should be suppressed, default False
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s AND MAJOR_NAME=%s AND MAJOR_YEAR=%s;'
        arguments = (student_id, major_name, major_year,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def remove_all_majors_from_student(self, student_id: int, *, suppress_commit=False):
        """ Removes all major information from the database for a student.

        :param student_id:      student's unique identifier
        :param suppress_commit: if autocommit should be suppressed, default False
        """
        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENT_MAJOR WHERE STUDENT_ID=%s;'
        arguments = (student_id,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()


    ### METHODS FOR THE STUDENTS TABLE ###


    def get_student(self, student_id: int, adviser_id: int = None) -> Student:
        """ Retrieves information stored for a student in the database.

        :param student_id: student's unique identifier
        :param adviser_id: adviser's unique identifier or None to ignore that field
        :return: retrieved student information or None if the student does not exist
        """

        ### Fetch the student's information stored within the STUDENT table ###

        cursor = self.db.cursor(buffered=True)

        if adviser_id is not None:
            sql_query = 'SELECT STUDENT_ID, ADVISOR_ID, FIRST, LAST, EMAIL, CLASSIFICATION, ' \
                        'GRAD_YEAR, GRAD_SEMESTER, ENROLLED_YEAR, ENROLLED_SEMESTER, ' \
                        'CREDITS_COMPLETED FROM STUDENTS WHERE STUDENT_ID=%s AND ADVISOR_ID=%s;'
            arguments = (student_id, adviser_id,)
        else:
            sql_query = 'SELECT STUDENT_ID, ADVISOR_ID, FIRST, LAST, EMAIL, CLASSIFICATION, ' \
                        'GRAD_YEAR, GRAD_SEMESTER, ENROLLED_YEAR, ENROLLED_SEMESTER, ' \
                        'CREDITS_COMPLETED FROM STUDENTS WHERE STUDENT_ID=%s;'
            arguments = (student_id,)

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

    def create_new_student(self, student: Student, remove_stale_majors=True, *, suppress_commit=False):
        """ Creates or updates information for a specific student.

        - Ensures the student's major exists when updating major information.
        - Optionally removes stale majors from the student_majors table.

        :param student:             dataclass containing the student's information
        :param remove_stale_majors: removes majors from a student that are not specified
                                    within the student object, default True
        :param suppress_commit:     if autocommit should be suppressed, default False
        """

        ### Create or update the information stored in the STUDENTS table ###

        cursor = self.db.cursor(buffered=True)

        sql_query = 'INSERT INTO STUDENTS (STUDENT_ID, ADVISOR_ID, FIRST, LAST, EMAIL, CLASSIFICATION, ' \
                    'GRAD_YEAR, GRAD_SEMESTER, ENROLLED_YEAR, ENROLLED_SEMESTER) VALUES (%s, %s, %s, %s, ' \
                    '%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE STUDENT_ID=VALUES(STUDENT_ID), ' \
                    'ADVISOR_ID=VALUES(ADVISOR_ID), FIRST=VALUES(FIRST), LAST=VALUES(LAST), ' \
                    'EMAIL=VALUES(EMAIL), CLASSIFICATION=VALUES(CLASSIFICATION), GRAD_YEAR=VALUES(GRAD_YEAR), ' \
                    'GRAD_SEMESTER=VALUES(GRAD_SEMESTER), ENROLLED_YEAR=VALUES(ENROLLED_YEAR), ' \
                    'ENROLLED_SEMESTER=VALUES(ENROLLED_SEMESTER);'
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
            student.enrolled_semester,)

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
            self.add_major_to_student(student_id, major_name, major_year, suppress_commit=True)

        # Remove extra majors from the student
        if remove_stale_majors:
            for major_name, major_year in existing_majors:
                self.remove_major_from_student(student_id, major_name, major_year, suppress_commit=True)

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def delete_student(self, student_id: int, adviser_id: int,
                       delete_majors=False, delete_schedules=False,
                       *, suppress_commit=False):
        """ Removes information about a student from the database.

        :param student_id:          student's unique identifier
        :param adviser_id:          adviser's unique identifier

        :param delete_majors:       if the student's major information should
                                    automatically be deleted from the STUDENT_MAJOR
                                    table to avoid a foreign key conflicts, default False

        :param delete_schedules:    if the student's schedules should automatically
                                    be deleted from the SCHEDULE table to avoid a foreign
                                    key conflict, default False

        :param suppress_commit:     if autocommit should be suppressed, default False

        :raises mysql.connector.errors.IntegrityError:
                if the student still has majors in the STUDENT_MAJOR table or if
                the student has schedules within the SCHEDULE table
        """

        if delete_majors is True:
            self.remove_all_majors_from_student(student_id, suppress_commit=True)

        if delete_schedules is True:
            self.delete_student_schedule(student_id, suppress_commit=True)

        cursor = self.db.cursor(buffered=True)

        sql_query = 'DELETE FROM STUDENTS WHERE STUDENT_ID=%s AND ADVISOR_ID=%s;'
        arguments = (student_id, adviser_id,)

        cursor.execute(sql_query, arguments)
        cursor.close()

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()

    def delete_advisers_students(self, adviser_id: int, delete_majors=False, delete_schedules=False,
                                 *, suppress_commit=False):
        """ Removes information for all students associated with an adviser.

        :param adviser_id:          adviser's unique identifier

        :param delete_majors:       if the student's major information should
                                    automatically be deleted from the STUDENT_MAJOR
                                    table to avoid a foreign key conflicts, default False

        :param delete_schedules:    if the student's schedules should automatically
                                    be deleted from the SCHEDULE table to avoid a foreign
                                    key conflict, default False

        :param suppress_commit:     if autocommit should be suppressed, default False

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
            self.delete_student(student_id, adviser_id, delete_majors, delete_schedules, suppress_commit=True)

        # commit the changes to the database
        if not suppress_commit and self.autocommit:
            self.db.commit()
