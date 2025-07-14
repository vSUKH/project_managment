from flask import Flask, render_template, request, redirect, url_for, session, flash
from Module import server

app = Flask(__name__)
app.secret_key = 'PasswordisVishal@12'
db = server.database()


@app.route('/addproject', methods=['GET', 'POST'])
def add_project():
    if 'admin' not in session:
        return redirect('/adminlogin')

    if request.method == 'POST':
        success = db.add_project(request.form)
        if success:
            flash('Project Added Successfully!', 'success')
        else:
            flash('Failed to Add Project!', 'error')
        return redirect(url_for('admin_dashboard'))

    return render_template('add_project.html')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/updateproject', methods=['GET', 'POST'])
def update_project():
    if request.method == 'POST':
        pid = request.form.get('project_id')  
        if pid:
           
            return "<h2 style='color:green;text-align:center;'>Updated Successfully!</h2>"
        else:
            return "<h2 style='color:red;text-align:center;'>Failed to Update</h2>"

    pid = request.args.get('pid') 
    return render_template('update_project.html', project_id=pid)


@app.route('/viewprojects')
def view_projects():
    result = db.view()
    return render_template('viewprojects.html', projects=result)

@app.route('/delete1/<int:project_id>/')
def delete1(project_id):
    print("project id=",project_id)
    data=db.Delete1(project_id)
    return redirect('/view')
  
@app.route('/addemployee', methods=['GET', 'POST'])
def addemployee():
    if request.method == 'POST':
        print("Form Data:", request.form)
        success = db.add_employee(request.form)
        if success:
            flash('Employee added successfully!', 'success')
        else:
            flash('Failed to add employee.', 'error')
        return redirect('/admin')  # redirect to dashboard or any desired page

    return render_template('add_employee.html')

@app.route('/viewemployees')
def view_employees():
    result = db.view_employee()  
    return render_template('view_employe.html', employees=result)

@app.route('/delete2/<int:eid>/')
def delete_employee(eid):
    db.delete_employee(eid)
    return redirect('/viewemployees')

@app.route('/employee_dashboard', methods=['GET', 'POST'])
def employee_dashboard():
    if 'employee' not in session:
        return redirect('/employeelogin')

    eid = session['employee']  # fetch eid from session
    dashboard_data = db.get_employee_dashboard_data(eid)

    if dashboard_data:
        return render_template('employee.html', **dashboard_data)
    else:
        return "<h3 style='color:red;'>Error: Could not load dashboard.</h3>"

@app.route('/employeelogin', methods=['GET', 'POST'])
def emp_login():
    if request.method == 'POST':
        username = request.form['eid']
        password = request.form['password']

        result = db.employee_login(username, password)

        if result:
            session['employee'] = username
            flash("Welcome! Login Successful ✅", "success")
            return redirect('/employee_dashboard')
        else:
            flash("Invalid username or password ❌", "error")
            return redirect(url_for('emp_login'))

    return render_template('employe_login.html')

@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        username = request.form['name']
        password = request.form['password']

        result = db.admin_login(username, password)

        if result:  # user found
            session['admin'] = username
            return redirect(url_for('admin_dashboard')) 
        else:
            return "<h3 style='color:red;text-align:center;'>Invalid username or password</h3>"
    
    return render_template('admin_login.html')  # Show login form

@app.route('/admin')
def admin_dashboard():
    con = db.connect()
    cursor = con.cursor()

    # Project stats (already working)
    cursor.execute("SELECT COUNT(*) FROM projects")
    total_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE deadline >= CURDATE()")
    active_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE deadline > CURDATE() AND proposed_project = 0")
    pending_projects = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM projects WHERE deadline < CURDATE()")
    overdue_projects = cursor.fetchone()[0]

    # ✅ Task stats
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE statuss = 1")
    completed_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE statuss = 0")
    pending_tasks = cursor.fetchone()[0]

    return render_template(
        'admin.html',
        total_projects=total_projects,
        active_projects=active_projects,
        pending_projects=pending_projects,
        overdue_projects=overdue_projects,
        total_tasks=total_tasks,
        completed_tasks=completed_tasks,
        pending_tasks=pending_tasks
    )

@app.route('/logout')
def logout():
    session.pop('admin', None)  
    return redirect('/')
    
@app.route('/assigntask', methods=['GET', 'POST'])
def add_task():
    con = db.connect()
    cursor = con.cursor()

    if request.method == 'POST':
        data = request.form
        try:
            query = """
                INSERT INTO tasks (project_id, task_id, descriptions, statuss, estimate_days, eid)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (
                data['project_id'],
                data['task_id'],
                data['descriptions'],
                int(data['statuss']),
                int(data['estimate_days']),
                data['eid']
            )
            cursor.execute(query, values)
            con.commit()
            flash("✅ Task Assigned Successfully", "success")
        except Exception as e:
            flash("❌ Failed to Assign Task: " + str(e), "error")
        return redirect(url_for('admin_dashboard'))  # Change if your admin route is different

    # GET method
    cursor.execute("SELECT eid, firstname, lastname FROM employee")
    employees = cursor.fetchall()

    cursor.execute("SELECT project_id, project FROM projects")
    projects = cursor.fetchall()

    return render_template('assigen_task.html', employees=employees, projects=projects)

@app.route('/viewtask',methods=['GET','POST'])
def view_tasks():
    data = db.get_all_tasks() 
    return render_template('view_task.html', tasks=data)

@app.route('/completed',methods = ['GET','POST'])
def complete():
    tasks = db.completed()
    return render_template('completed.html', tasks=tasks)
  
@app.route('/pending',methods = ['GET','POST'])
def pending():
    tasks = db.pending()
    return render_template('pending.html', tasks=tasks)

@app.route('/profile',methods = ['GET','POST'])
def emp_profile():
    eid = session['employee']
    data = db.get_employee_profile(eid)
    return render_template('employee_profile.html',profile = data)  

@app.route('/myprojects',methods=['GET','POST'])
def emp_projec():
    eid = session['employee']
    result = db.get_employee_projects(eid)
    return render_template('employe_projects.html', projects=result)

@app.route('/changestatus', methods=['GET'])
def change_status():
    pid = request.args.get('pid')

    if not pid:
        flash("Invalid Project ID!", "danger")
        return redirect('/empprojects')

    try:
        db.update_project_status(pid)
        flash("✅ Project marked as completed.", "success")
    except Exception as e:
        flash(f"❌ Failed to update: {str(e)}", "danger")

    return redirect('/myprojects')

@app.route('/deadlines')
def deadlines():
    return "<h3>Coming soon...</h3>"

@app.route('/notification',methods=['GET','POST'])
def notifications():
    return render_template('emp_notification.html')

if __name__ =='__main__':
    app.run(debug=True)


