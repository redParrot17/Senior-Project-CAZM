import mysql.connector



class Database:

    def __init__(self, config_file='mysql.cnf'):
        self.db = mysql.connector.connect(option_files=config_file, autocommit=True)

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

    def search_course_codes(self, argument1):
         cursor = self.db.cursor(buffered=True)
         arg1 = argument1 + "%"
         arg2 = arg1
         args = (arg1,arg2)
         sql = 'SELECT COURSE_CODE, NAME, YEAR, SEMESTER FROM COURSE WHERE COURSE_CODE LIKE %s OR NAME LIKE %s;'
         cursor.execute(sql, args)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, name, year, semester in results:
             course_info.append({"course_code":course_code,"name":name,"year": year, "semester": semester})
         return course_info

    def get_all_courses(self):
         cursor = self.db.cursor(buffered=True)
         sql = 'SELECT COURSE_CODE, YEAR, SEMESTER FROM COURSE;'
         cursor.execute(sql)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, year, semester in results:
             course_info.append({"courseCode": course_code, "year":year, "semester":semester})
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
