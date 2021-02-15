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
        result = cursor.fetchall()

        # close the cursor
        cursor.close()

        # do something with the results
        return_value = []
        for foo, bar in results:
            return_value.append([foo, bar])
        return return_value

    def search_course_codes(self, argument1):
         cursor = self.db.cursor(buffered=True)

         args = argument1 + "%"
         sql = 'SELECT COURSE_CODE, YEAR, SEMESTER FROM COURSE WHERE COURSE_CODE LIKE "%s";'
         cursor.execute(sql, args)
         results = cursor.fetchall()
         cursor.close()

         course_info = []
         for course_code, year, semester in results:
             course_info.append([course_code, year, semester, argument1])
         return course_info