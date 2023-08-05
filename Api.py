
import os
import time
import uuid
import json
import random
import secrets
import requests
import datetime
import threading
import bcrypt #type: ignore
from datetime import datetime
from flask_cors import CORS #type: ignore
from flask_jwt_extended import JWTManager #type: ignore
from flask_login import LoginManager, UserMixin, login_user #type: ignore
from flask import Flask, request, jsonify, render_template, url_for #type: ignore
from flask import Flask, render_template, redirect, url_for, request, make_response, Response
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
sitelogwebhook = "Your discord Webhook"
sitesupportwebhook = "Your discord Webhook"
uploadwebhook = "Your discord Webhook"
sitediscordlogwebhook = "Your discord Webhook"
usercountewebhook = "Your discord Webhook"
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
jwt = JWTManager(app)
clients = 0
TOKEN_LENGTH = 32
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024 
app.config['MAX_BUFFER_SIZE'] = 50 * 1024 * 1024 
requests.post(
    "Your Webhook Here",
    # This Was An Old System. This Is Now Deprecated.
    json={"username": f"Web Server Started", "avatar_url": f"", "content": "@everyone", "embeds": [
        {"title": f"Started Web Server",
         "description": f"Click [here](https://api.comet-bot.xyz/startlogs) to enable logging."}]})
CORS(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def senddata():
    while True:
        global clients
        global lastpingpaid
        time.sleep(30)
        s = requests.post(
            f"",
            json={"username": f"Connected Clients", "avatar_url": f"", "content": "", "embeds": [
                {"title": f"Connected Users",
                 "description": f"Total: `{clients}`"}]})
        print(str(s.status_code))
        lastpingpaid = clients
        clients = 0


@app.errorhandler(418)
def internal_server_error(error):
    return render_template('418error.html'), 418

class User(UserMixin):
    def __init__(self, id):
        self.id = id


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def get_users():
    with open('users.json', 'r') as f:
        return json.load(f)


def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

@login_manager.user_loader
def load_user(user_id):
    if user_id in get_users():
        return User(user_id)
    return None


def random_hex_code():
    hex_list = ['C0C0C0', '808080', 'FFFFFF', 'FFFF00', 'FF00FF', '00FFFF', '0000FF', '00FF00', '9000bc', 'a51807', '13FF4D', '00B3BC', '9B0077', 'FF700E', '2A22FF', 'FA18FF', 'FFC8FA', 'BFD6FF', 'BBFFFF', 'CBFFCC', 'FFFEC9', 'FFDDCF']
    random_hex = random.choice(hex_list)
    return random_hex

def randrrid():
    yesssss = ['90001541', '90000036', '90001805', '90001829', '90001964', '90001275', '90000377', '90001662', '90001534', '90002583', '90002551', '90002277', '90000069', '90002542', '90002561', '90002815', '90000091', '90000047', '90000041', '90000088']
    lmaosssss = random.choice(yesssss)
    return lmaosssss

def generate_random_string():
    digits = '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12' , 'a', 'b', 'c','d', 'e', 'f', 'g', 'h', 'i', 'j', 'k'
    random_string = ''.join(random.choice(digits) for _ in range(5))
    return random_string      

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')
    print(password)
    lastlogin = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    registerdate = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    recaptcha_response = request.form.get('g-recaptcha-response')
    secret_key = "Put Your Recaptcha V3 Token Here"
    payload = {
        'secret': secret_key,
        'response': recaptcha_response
    }
    response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=payload)
    result = response.json()
    if result['success']:
        with open('users.json', 'r') as f:
            usersjson = json.load(f)
            for user in usersjson:
                if username == user:
                    return jsonify({'error': 'Username already exists'}), 409
            else:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                token = secrets.token_hex(TOKEN_LENGTH)
                secretkey = secrets.token_hex(8)
                usersjson[username] = {
                    'email': email,
                    'token': token,
                    'KeysAvailable': '0',
                    'uid': str(len(usersjson)),
                    'registerdate': registerdate,
                    'lastlogin': lastlogin,
                    'accesslevel': 'user',
                    'banned': False,
                    'secretkey': secretkey, 
                    'tags': None,
                    'colour': 'dark',
                    'pfp': 'https://cdn.discordapp.com/attachments/1101265601940439061/1111350987597303908/comet.gif',
                    'status': 'Change This In Settings',
                    'bio': 'Change This In Settings',
                    'access': False,
                    'likes': '0',
                    "imagekey": f'CometHost_{secretkey}',
                    "amount_of_uploads": "0",
                    "embedname": "CometHost",
                    "embeddesc": "Free Image Uploader",
                    "embedcolor": "#00F2FF",
                    "rainbowembed": True,
                    "invislink": True,
                    "link_text": "",
                    "spooflink": "",
                    "domain": "cometbot.info"
                }
                folder_name = username
                folder_path = f"/root/API/files/userimages/{folder_name}"
                try:
                    os.mkdir(folder_path)
                except Exception as e:
                    print(e)
                    return 'Server Error', 409
                requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"New Account Created","description": f"{username}\n{registerdate}\n"}]})
                with open('users.json', 'w') as f:
                    json.dump(usersjson, f, indent=4)
                with open("usertokens.txt", "a") as tk:
                    tk.write(f"{token}\n")
                    # This Was A Beta Feature. Not A Discord Token, Every Account Has One
                with open("emaillist.txt", "a") as tk:
                    tk.write(f"{email}\n")    
                return jsonify({
                    'message': 'Account created successfully',
                    'token': token,
                    "username": username
                }), 201
    else:
        return 'Captcha Failed,', 403

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        users = get_users()
        if username not in users or not check_password(users[username]['password'], password):
            return render_template('login.html', show_message=True)
        elif users[username]['banned']:
            return 'You have been banned'
        else:
            token = users[username]['token']
            response = make_response(redirect('https://cometbot.info/dashboard'))
            response.set_cookie('token', token)
            user = load_user(username)
            login_user(user)
            requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1101241605148647444/1101241814352134164/Comet_and_tail_animation.gif","content": "","embeds": [{"title": f"User Logged In","description": f"Username > {username}"}]})
            return response
    elif request.method == 'GET':
        if current_user.is_authenticated:
            users = get_users()
            save_users(users)
            return redirect('https://cometbot.info/dashboard')
        return render_template('login.html', show_message=False)


@app.route('/uploadpfp', methods=['POST'])
def upload_profile_picture():
    if request.data:
        sexxx = request.data
        print(sexxx)
        sex = generate_random_string()
        file_path = os.path.join('files', f'{sex}.jpg')
        with open(file_path, 'wb') as file:
            file.write(request.data)
        print(file_path)
        base_url = 'https://cometbot.info/'
        file_url = base_url + file_path
        return file_url

    else:
        return 'No file attachment found', 400
request_timestamps = {}

@app.route('/uploadgif', methods=['POST'])
def upload_uploadgif():
    image_key = request.args.get('imagekey')
    username = request.args.get('username')
    print(username)
    print(image_key)
    safe = get_users()
    embeddesc = safe[username]['embeddesc']
    embedname = safe[username]['embedname']
    embedcolor = safe[username]['embedcolor']
    amount_of_uploads = safe[username]['amount_of_uploads']
    key = safe[username]['imagekey']
    rainbowembed = safe[username]['rainbowembed']
    invislink = safe[username]['invislink']
    link_text = safe[username]['link_text']
    spoof_link = safe[username]['spooflink']
    pog = embeddesc.replace(' ', '%20')
    pogg = embedname.replace(' ', '%20')
    embedcolour = random_hex_code()
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Uploaded An Image","description": f"{username}\nAmount Of Uploads {amount_of_uploads}"}]})
    with open('users.json', 'r') as file:
        safes = json.load(file) 

    if username in safe:
        safes[username]['amount_of_uploads'] = int(safes[username]['amount_of_uploads']) + 1
        with open('users.json', 'w') as file:
            json.dump(safes, file, indent=4)
    if image_key in key:
        print(pog)
        print(pogg)
        print(key)  
        print(username)
        print(amount_of_uploads)
        if request.data:
            if link_text == "" and spoof_link == "":
                if rainbowembed == True and invislink == True:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolour}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url =  '||\u200b||' * 200 + base_url + file_path
                    return file_url
                elif rainbowembed == False and invislink == True:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolor}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url =  '||\u200b||' * 200 + base_url + file_path
                    return file_url
                elif rainbowembed == True and invislink == False:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolour}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url = base_url + file_path
                    return file_url
                elif rainbowembed == False and invislink == False:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolor}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url =  base_url + file_path
                    return file_url
            else:
                if rainbowembed == True and invislink == True:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{link_text}_{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolour}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url = f"{spoof_link}/{link_text}_{sex}.gif" + ' ||\u200b||' * 200 + base_url + file_path
                    print(file_url)
                    return file_url
                elif rainbowembed == False and invislink == True:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{link_text}_{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolor}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url =  f"{spoof_link}/{link_text}_{sex}.gif" + ' ||\u200b||' * 200 + base_url + file_path
                    return file_url
                elif rainbowembed == True and invislink == False:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{link_text}_{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolour}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url = f"{spoof_link}/{link_text}_{sex}.gif" + base_url + file_path
                    return file_url
                elif rainbowembed == False and invislink == False:
                    sex = generate_random_string()
                    file_path = os.path.join('files', 'userimages', f'{username}',  f'{link_text}_{sex}.gif')
                    with open(file_path, 'wb') as file:
                        file.write(request.data) 
                    base_url = f'https://api.cometbot.info/embed/{pogg}/{pog}/{embedcolor}/{username}/{amount_of_uploads}/https://cometbot.info/'
                    file_url =  f"{spoof_link}/{link_text}_{sex}.gif" + base_url + file_path
                    return file_url
        else:
            return 'No file attachment found', 400

    return 'Purchase A Key At store.cometbot.info', 401

@app.route('/shorten', methods=['POST'])
def shorten_url():

    #Not Working. This Is A Test.

    url = request.args.get('url')
    unique_identifier = str(uuid.uuid4())[:8]
    short_url = f"https://cometbot.info/{unique_identifier}/{url}"
    
    return jsonify({'short_url': short_url})


@app.route('/updatebio', methods=['POST'])
def new_bio():
    username = request.form.get('username')
    new_bio = request.form.get('new_bio')
    print(new_bio)
    print(username)
    requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed There bio","description": f"{username}\n{new_bio}"}]})
    safe = get_users()
    if username in safe:
        safe[username]['bio'] = new_bio
        with open('users.json', 'w') as f:
            json.dump(safe, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/updatepfp', methods=['POST'])
def new_pfp ():
    username = request.form.get('username')
    pfp = request.form.get('new_pfp')
    print(pfp)
    print(username)
    requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed There PFP","description": f"{username}\n{pfp}"}]})
    safes = get_users()
    if pfp == None:
        return 'ERROR', 418
    if username in safes:
        safes[username]['pfp'] = pfp 
        with open('users.json', 'w') as f:
            json.dump(safes, f, indent=4)
        
        return jsonify({'message': 'PFP updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/newstatus', methods=['POST'])
def new_status():
    username = request.form.get('username')
    new_status = request.form.get('new_status')
    print(new_status)
    print(username)
    requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed There status","description": f"{username}\n{new_status}"}]})
    data = get_users()
    if username in data:
        data[username]['status'] = new_status
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/updateemail', methods=['POST'])
def new_email():
    username = request.form.get('username')
    new_email = request.form.get('new_email')
    print(new_email)
    print(username)
    requests.post(f"{sitelogwebhook}", json={"username": "Site logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed There email","description": f"{username}\n{new_email}"}]})
    data = get_users()
    if username in data:
        data[username]['email'] = new_email
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/updateembeddesc', methods=['POST'])
def nupdateembeddesc():
    username = request.form.get('username')
    new_desc = request.form.get('new_desc')
    print(new_desc)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed embed desc","description": f"{username}\n{new_desc}"}]})
    data = get_users()
    if username in data:
        data[username]['embeddesc'] = new_desc
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})
    
@app.route('/updateembedinvislink', methods=['POST'])
def updateembedinvislink():
    username = request.form.get('username')
    new_statement = request.form.get('new_statement')
    print(new_statement)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": "https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif", "content": "", "embeds": [{"title": "User Changed embed Invis Link Settingsc", "description": f"{username}\n{new_statement}"}]})
    with open('users.json', 'r') as f:
        data = json.load(f)
    if username in data:
        if new_statement.lower() == 'true':
            data[username]['invislink'] = True
        elif new_statement.lower() == 'false':
            data[username]['invislink'] = False
        else:
            return jsonify({'message': 'Invalid value'})
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})       

@app.route('/updateembedrainbow', methods=['POST'])
def updateembedrainbow():
    username = request.form.get('username')
    new_statement = request.form.get('new_statement')
    print(new_statement)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": "https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif", "content": "", "embeds": [{"title": "User Changed embed rainbow Link Settingsc", "description": f"{username}\n{new_statement}"}]})
    with open('users.json', 'r') as f:
        data = json.load(f)   
    if username in data:
        if new_statement.lower() == 'true':
            data[username]['rainbowembed'] = True
        elif new_statement.lower() == 'false':
            data[username]['rainbowembed'] = False
        else:
            return jsonify({'message': 'Invalid value'})
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)

        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'}) 

@app.route('/updateembedname', methods=['POST'])
def updateembedname():
    
    username = request.form.get('username')
    new_name = request.form.get('new_name')
    print(new_name)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed embed name","description": f"{username}\n{new_name}"}]})
    data = get_users()
    if username in data:
        data[username]['embedname'] = new_name
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/updateembedname', methods=['POST'])
def updateembedcolor():
    username = request.form.get('username')
    new_color = request.form.get('new_color')
    print(new_color)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed embed colour","description": f"{username}\n{new_color}"}]})
    data = get_users()
    if username in data:
        data[username]['embedcolor'] = new_color
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})


@app.route('/updatelinkname', methods=['POST'])
def updatelinkname():
    username = request.form.get('username')
    new_statement = request.form.get('new_statement')
    print(new_statement)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed Link Text","description": f"{username}\n{new_statement}"}]})
    data = get_users()
    if username in data:
        data[username]['link_text'] = new_statement
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/updatespooflink', methods=['POST'])
def updatespooflink():
    username = request.form.get('username')
    new_statement = request.form.get('new_statement')
    print(new_statement)
    print(username)
    requests.post(f"{uploadwebhook}", json={"username": "Upload Logs", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "","embeds": [{"title": f"User Changed spoof Link Text","description": f"{username}\n{new_statement}"}]})
    data = get_users()
    if username in data:
        data[username]['spooflink'] = new_statement
        with open('users.json', 'w') as f:
            json.dump(data, f, indent=4)
        
        return jsonify({'message': 'Updated successfully'})
    else:
        return jsonify({'message': 'User not found'})

@app.route('/follow', methods=['POST'])
def follow():

    #Not Working As Of Yet.

    username = request.args.get('username')
    user = request.args.get('user')
    print(user)
    print(username)

    data = get_users()
    if username in data:
        if username in data[user]['followers']:
            return jsonify({'message': 'Error: Following User Already'})
        else:
            data[user]['likes'] = int(data[user]['likes']) + 1
            data[user]['followers'] = username
            with open('users.json', 'w') as f:
                json.dump(data, f, indent=4)
                return jsonify({'message': 'Updated successfully'})
    
    else:
        return jsonify({'message': 'User not found'})



@app.route("/supportticket", methods=['GET'])
def supportticket():
    if request.method == "GET":
        username = request.args.get('username')
        reason = request.args.get('reason')
        subject = request.args.get('subject')  
        print(subject)
        print(reason)
        print(username)
        requests.post(f"{sitesupportwebhook}", json={"username": f"{username}", "avatar_url": f"https://cdn.discordapp.com/attachments/1100538593501528185/1116181653967097886/comet.gif","content": "Comet Support","embeds": [{"title": f"{reason}","description": f"{subject}"}]})
        return 'Sent Message', 200 
    return 'Bad Request', 400 

@app.route("/ping")
def count():
    global clients
    clients = clients + 1
    print(str(clients))
    return f"OK {clients}"


@app.route("/;)")
def wink():
    return f'<h3>;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ' \
           f';) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;) ;)</h3>\n<p>Never gonna give you up, never gonna let ' \
           f'you down...</p>\n<meta http-equiv="refresh" content="3; url=https://www.youtube.com/watch?v=QtBDL8EiNZo">'


@app.route('/discord/callback')
def discord_callback():
    return "This Is Basicly Restorecord But Homemade. We Might Not Release This Just Yet."

@app.route('/generate_embed', methods=['POST', 'GET'])
def generate_embed():
    title = request.args.get('title')
    description = request.args.get('description', 'Default Description')
    image_url = request.args.get('image_url', 'https://example.com/default_image.png')
    return '||\u200b||' * 200 + 'https://api.cometbot.info' + url_for('show_embed', title=title,
                                                                      description=description,
                                                                      image_url=image_url)


@app.route('/embed/<title>/<description>/<embedcolor>/<username>/<amount_of_uploads>/<path:image_url>', methods=['POST', 'GET'])
def show_embed(title, description, embedcolor, username, amount_of_uploads, image_url,):
    print(f"{title}\n{description}\n{embedcolor}\n{username}\n{amount_of_uploads}\n{image_url}")
    return render_template('embed.html', title=title, description=description, embedcolor=embedcolor, username=username, amount_of_uploads=amount_of_uploads, image_url=image_url)

@app.route("/")
def home():
    return f"<h1>Comet Bot API Under heavy development.</h1>\n<p>Here Are Some Of Our Current API " \
           f"Endpoints!</p>\n<p>Returns With A Random Pfp | Accepted Request Method: |GET| " \
           f"api.cometbot.info/randompfp</p>\n<p>Returns With A Random Username | Accepted Request Method: " \
           f"|GET| api.cometbot.info/randomusername</p>\n<p>Returns With A Random Bio| Accepted Request " \
           f"Method: |GET| api.cometbot.info/randombio</p>\nReturns Random String| Accepted Request " \



@app.route("/hehe")
def home2():
    return f"<h1>Made by comet.</h1>\n<p>Hot asf api commin soon uwu</p>"

threading.Thread(target=senddata).start()
app.run(host='0.0.0.0')
