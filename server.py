import pymysql
import pymysql.cursors

class database:
    def connect(self):
        print("Sever connected!")
        return pymysql.connect(host="localhost", user="root", password="root", database="project_managment")
    
    def add_project(self, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO projects (project_id, project, location, overall_cost, start_date, deadline, tid, proposed_project, date_added) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    int(data['project_id']),
                    data['project'],
                    data['location'],
                    int(data['overall_cost']),
                    data['start_date'],
                    data['deadline'],
                    int(data['tid']),
                    int(data['proposed_project']),
                    data['date_added'] ))
            con.commit()
            return True
        except Exception as e:
            print("Error:", str(e))
            con.rollback()
            return False
        finally:
            con.close()

    def update_project(self, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            # Step 1: Check if the project exists
            cursor.execute("SELECT * FROM projects WHERE project_id = %s", (int(data['project_id']),))
            result = cursor.fetchone()
            if not result:
                print(f"Project ID {data['project_id']} does not exist.")
                return False

            # Step 2: Proceed to update
            cursor.execute(
                """
                UPDATE projects
                SET project = %s,
                    location = %s,
                    overall_cost = %s,
                    start_date = %s,
                    deadline = %s,
                    tid = %s,
                    proposed_project = %s,
                    date_added = %s
                WHERE project_id = %s
                """,
                (
                    data['project'], data['location'], int(data['overall_cost']),
                    data['start_date'], data['deadline'], int(data['tid']),
                    int(data['proposed_project']), data['date_added'],
                    int(data['project_id'])
                )
            )
            con.commit()
            return True

        except Exception as e:
            print("Update Error:", str(e))
            con.rollback()
            return False
        finally:
            con.close()

    def view(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "SELECT * FROM projects"
            cursor.execute(query)
            result = cursor.fetchall()
            print("Fetched Projects:", result)
            return result 
        except Exception as e:
            print("Error", str(e))
            return []      
        finally:
            con.close()

    def Delete1(self, data):
        print("work1")
        con = self.connect()
        print("work2")
        cursor = con.cursor()
        print("work3")
        try:
            quarry = "delete from projects where project_id = "+ str(data)
            print(quarry)
            cursor.execute(quarry)                        
            con.commit()
        except Exception as e :
            print("Error",str(e))

        finally:
            con.close()

    def add_employee(self, data):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute(
                "INSERT INTO employee (eid, lastname, firstname, bday, contact_no, address, pid, statuss, gender, date_added,password) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)",
                (
                    data['eid'],
                    data['lastname'],
                    data['firstname'],
                    data['bday'],
                    data['contact_no'],  
                    data['address'],
                    data['pid'],
                    data['statuss'],
                    data['gender'],
                    data['date_added'],
                    data['password']
                )
            )
            con.commit()
            return True
        except Exception as e:
            print("Error:", str(e))
            con.rollback()
            return False
        finally:
            con.close()

    def admin_login(self, name, password):
        con = self.connect()
        cursor = con.cursor()
        try: 
            cursor.execute("SELECT * FROM addmin WHERE firstname = %s AND password = %s", 
                           (name,password))
            return cursor.fetchall()
        except Exception as e:
            print("Login error:", e)
            return ()
        finally:
            con.close()
        
    def view_employee(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM employee")
            data = cursor.fetchall()
            return data
        except Exception as e:
            print("Error:", str(e))
            return []
        finally:
            con.close()
    
    def delete_employee(self, eid):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("DELETE FROM employee WHERE eid = %s", (eid,))
            con.commit()
        except Exception as e:
            print("Delete Error:", e)
        finally:
            con.close()

    def employee_login(self, eid, password):
        con = self.connect()
        cursor = con.cursor()
        try: 
            cursor.execute("SELECT * FROM employee WHERE eid = %s AND password = %s", 
                           (eid,password))
            return cursor.fetchall()
        except Exception as e:
            print("Login error:", e)
            return ()
        finally:
            con.close()
        
    def get_employee_dashboard_data(self, eid):
        con = self.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            # Get employee full name
            name_query = "SELECT firstname, lastname FROM employee WHERE eid = %s"
            cursor.execute(name_query, (eid,))
            emp = cursor.fetchone()
            employee_name = f"{emp['firstname']} {emp['lastname']}" if emp else "Employee"

            # Get distinct projects the employee is working on (via tasks)
            project_query = """
                SELECT DISTINCT p.project AS name,
                                CASE
                                    WHEN t.statuss = 1 THEN 'Completed'
                                    ELSE 'Pending'
                                END AS status
                FROM tasks t
                JOIN projects p ON t.project_id = p.project_id
                WHERE t.eid = %s
            """
            cursor.execute(project_query, (eid,))
            projects = cursor.fetchall()

            # Calculate stats
            total_projects = len(projects)
            completed_projects = sum(1 for p in projects if p['status'].lower() == 'completed')
            pending_projects = total_projects - completed_projects

            return {
                'employee_name': employee_name,
                'projects': projects,
                'total_projects': total_projects,
                'completed_projects': completed_projects,
                'pending_projects': pending_projects
            }
        except Exception as e:
            print("Dashboard Error:", e)
            return None
        finally:
            con.close()


    def get_all_tasks(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            cursor.execute("SELECT * FROM tasks")
            data = cursor.fetchall()
            return data
        except Exception as e:
            print("Error fetching projects:", e)
            return []
        finally: 
            con.close()

    def completed(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "SELECT * FROM tasks where statuss = 1"
            cursor.execute(query)
            result = cursor.fetchall()
            print("Fetched Projects:", result)
            return result 
        except Exception as e:
            print("Error", str(e))
            return []      
        finally:
            con.close()     

    def pending(self):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "SELECT * FROM tasks where statuss = 0"
            cursor.execute(query)
            result = cursor.fetchall()
            print("Fetched Projects:", result)
            return result 
        except Exception as e:
            print("Error", str(e))
            return []      
        finally:
            con.close()   

    def get_employee_profile(self,eid):
        con = self.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            cursor.execute("Select * from employee where eid = %s",(eid,))
            return cursor.fetchone()
        except Exception as e:
            print("Error",str(e))
        finally:
            con.close()

    def get_employee_projects(self, eid):
        con = self.connect()
        cursor = con.cursor(pymysql.cursors.DictCursor)
        try:
            query = """
                SELECT DISTINCT p.*
                FROM projects p
                JOIN tasks t ON p.project_id = t.project_id
                WHERE t.eid = %s
            """
            cursor.execute(query, (eid,))
            return cursor.fetchall()
        except Exception as e:
            print("Error:", str(e))
            return []
        finally:
            con.close()
        
    def update_project_status(self, project_id):
        con = self.connect()
        cursor = con.cursor()
        try:
            query = "UPDATE projects SET proposed_project = 1 WHERE project_id = %s"
            cursor.execute(query, (project_id,))
            con.commit()
        except Exception as e:
            print("Status Update Error:", e)
            con.rollback()
            raise
        finally:

            con.close()

