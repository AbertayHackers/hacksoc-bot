import re, asyncio
from secrets import token_hex as genToken
from flask import Flask, request, session, render_template, flash, redirect, url_for, Markup
from flask_limiter import Limiter
from validate_email import validate_email as valEmail
from datetime import timedelta, datetime
from time import time
from libs.loadconf import secrets
from libs.genInvite import genInvite
from libs.saferproxyfix import SaferProxyFix
from libs.db import SignupConn
from libs.sendMail import SendMail


limiter = Limiter(key_func=lambda:request.headers.get("X-Forwarded-For"))
app = Flask("InviteSite")
app.template_folder="inviteSite/views"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(hours=6)
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SECRET_KEY"] = secrets["flaskSecret"]
app.wsgi_app = SaferProxyFix(app.wsgi_app)
limiter.init_app(app)

@app.route("/")
def registerHome():
    return render_template("display.html", page="home.html"), 200

@app.route("/verify")
def verify():
    return render_template("display.html", page="verify.html"), 200

@app.route("/", methods=["POST"])
@limiter.limit("3/hour,1/second")
def registerLogic():
    studentID = request.form.get("studentID")
    if studentID: studentID = re.sub("[^0-9]", "", studentID)
    if not studentID or len(studentID) != 7:
        flash("Invalid Student ID")
        return redirect("/"), 302        
    #Check to see if there's already an active invite
    conn = SignupConn()    
    if conn.checkPreviousSignup(studentID):
        flash("Your student ID has already been used to join the Discord server. Please email us if this is a mistake.")
        return redirect("/")
    elif conn.checkValidInvites(studentID):
        flash(Markup("You already have an active invite pending verification.<br>Please <a href='/resend'>request a new email</a> if you haven't received a verification email in your university account"))
        return redirect(url_for("verify"))
    

    email = studentID + "@uad.ac.uk"
    if not valEmail(email_address=email):
        flash("Invalid Student ID or your email address hasn't been set up yet. If this is an error, please email us on the address above.")
        return redirect("/"), 302        

    #Generate a verification token
    token = genToken(8)
    print(token) #Used for debugging
    
    #Ascertain role to be member or fresher
    perm = "fresher" if str(datetime.now().year)[2:] == studentID[:2] else "member"
    rowID = conn.autoInvite(studentID, perm, token)
    if not rowID:
        flash("Something went wrong! Please email us")
        return redirect(url_for("registerHome"))
    session["registerID"] = rowID
    return redirect(url_for("verify"))


@app.route("/verify", methods=["POST"])
@limiter.limit("3/hour,1/second")
def verifyToken():
    token = request.form.get("code")
    registerID = session.get("registerID")
    if not token or len(token) != 16:
        flash("Invalid token")
        return redirect(url_for("verify"))
    elif not registerID:
        flash("No ID found. Please make sure that you have cookies enabled")    
        return redirect(url_for("verify"))

    conn = SignupConn()
    codeInfo = conn.checkVerificationCode(registerID)
    if not codeInfo:
        flash(Markup("""Code not found.<br>
                    This can happen if the code does not exist, or has already been used.<br>
                    Please email us on <a href="team@hacksoc.co.uk">team@hacksoc.co.uk</a> if this is not the case."""))
        return redirect(url_for("verify"))

    if int(time()) > int(codeInfo["verificationExpiry"]):
        flash("Verification code expired. Please try again")
        return redirect("/")
    elif token != codeInfo["verificationCode"]:
        flash("Incorrect Token")
        return redirect(url_for("verify"))
    conn.setVerificationUsed(registerID)
    code = genInvite()
    conn.insertInvite(registerID, code)
    if code:
        return redirect(f"https://discord.gg/{code}")
    flash("Failed to generate invite!")
    return redirect(url_for("verify"))

@app.route("/resend", strict_slashes=False)
def resend():
    return "True"
