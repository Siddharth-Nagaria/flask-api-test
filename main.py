from flask import Flask, jsonify, render_template, request, redirect, session
app=Flask(__name__)

@app.route('/')
def hello_test():
    return "Hi, Welcome to Unit testing"

@app.route('/login/<name>')
def view_form(name):
    return render_template('login.html', name=name)

@app.route('/factorial/<int:n>')
def factorial(n):
    ans = 1
    
    for i in range(2, n + 1):
        ans *= i
    
    result ={
        "number": n,
        "factorial": ans
    }
    return jsonify(result)

 
app.secret_key = 'my_secret_key'
users = {
    'siddharth': '1234',
    'harsh': '5678'
}
 
@app.route('/handle_get', methods=['GET'])
def handle_get():
    if request.method == 'GET':
        username = request.args['username']
        password = request.args['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')
 

@app.route('/handle_post', methods=['POST'])
def handle_post():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        if username in users and users[username] == password:
            return '<h1>Welcome!!!</h1>'
        else:
            return '<h1>invalid credentials!</h1>'
    else:
        return render_template('login.html')
    

if __name__ == "__main__":
    app.run(debug=True)