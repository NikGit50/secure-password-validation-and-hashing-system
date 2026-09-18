import hashlib
import os.path
from flask import Flask, request, render_template

app = Flask(__name__)

def block(password):
    # Safely create the blocked file if it doesn't exist
    if not os.path.exists("blocked_password.txt"):
        with open("blocked_password.txt", "w") as file:
            print("blocked_password.txt file created")
            
    with open("blocked_password.txt", "r") as file:
        check = file.read().splitlines()
        
    if password in check:
        print("Password is already blocked.")
        return " (Already Blocked)"
    else:
        with open("blocked_password.txt", "a") as file:
            file.write(password + "\n")
        print("Password is now blocked.")
        return " (Added to Blocked List)"

def password_checker(password):
    # 1. Length Checks
    if len(password) < 8:   
        msg = "Password must be at least 8 characters long."
        return msg + block(password)
    
    elif len(password) > 12:   
        msg = "Password must be maximum 12 characters long."
        return msg + block(password)
    
    # 2. Character Rules Checks
    elif not any(char.isupper() for char in password):   
        msg = "Password must contain at least one uppercase letter."
        return msg + block(password)
    
    elif not any(char.islower() for char in password):   
        msg = "Password must contain at least one lowercase letter." 
        return msg + block(password) 
    
    elif not any(char.isdigit() for char in password):   
        msg = "Password must contain at least one digit."  
        return msg + block(password)
    
    elif not any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/" for char in password):   
        msg = "Password must contain at least one special character."
        return msg + block(password)
    
    # 3. Successful Valid Password Handling
    else:
        print("Password is valid.")
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        print("Hashed password:", hash_password)
        with open("valid_password.txt", "a") as file:
            file.write(hash_password + "\n")
        return f"Password is valid. Saved Hash: {hash_password}"

@app.route('/', methods=['GET', 'POST'])
def submit():
    message = None
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password:
            message = password_checker(password)
        else:
            message = "Please enter a password."
    return render_template('form.html', message=message)

if __name__ == '__main__':
    app.run(debug=True)
