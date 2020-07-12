from flask import Blueprint, render_template, redirect, request, session, Response
from flask import current_app as app 
from .flask_spotify_auth import getUserToken, getUser 
from .funcs import get_playlists, get_pl_items, get_audio_features, make_df, get_user_id, generate_cl_pls
from .forms import *
from .model import cluster_pl

# Set up blueprint
main_bp = Blueprint("main_bp", __name__,
                    template_folder="templates",
                    static_folder="static")

@main_bp.route("/")
def home():
    return render_template("home.jinja2")

@main_bp.route("/login")
def login():
    response = getUser()
    return redirect(response)

@main_bp.route("/callback/")
def callback():
    TOKEN = getUserToken(request.args['code'])
    session["auth_head"] = TOKEN[1]
    session["user_id"] = get_user_id(session["auth_head"])["id"]
    return redirect("/playlist")

@main_bp.route("/playlist", methods=['post','get'])
def playlist():
    session["pl_items"] = get_playlists(session["auth_head"])["items"]
    choices = [(item["id"], item["name"]) for item in session["pl_items"]]
    totals = [item["tracks"]["total"] for item in session["pl_items"]]
    form = make_pl_form(choices)

    if form.validate_on_submit() and len(form.pls.data) > 0:
        session["pl_ids"] = form.pls.data
        return redirect("/cluster")  

    else:
        print("Validation Failed")
        print(form.errors)
    return render_template('playlist-form.jinja2',form=form, totals=totals)

@main_bp.route("/cluster", methods=['get'])
def cluster():
    session["pl_items"], id_list = get_pl_items(session["auth_head"], session["pl_ids"])
    print(session["pl_ids"])
    print(len(id_list))
    session["audio_features"] = get_audio_features(session["auth_head"], id_list)

    df = make_df(session["pl_items"], session["audio_features"])
    session["cl_list"], session["track_names"]= cluster_pl(df)
    return redirect("/tracks")

@main_bp.route("/tracks", methods=['post', 'get'])
def tracks():
    choices = []
    for i in range(len(session["cl_list"])):
        choices.append((str(i), session["cl_list"][i]))    

    emojis = ["🍭", " 🦩", "🌈", "☀️", "⚡️", "❤️", "🍌", "🍉", "🧁", "🍻"]

    form = list_form(choices)

    if form.validate_on_submit() and len(form.multicheck.data) > 0:
        print("formdata:")
        print(form.multicheck.data)  
        chosen_lists = [session["cl_list"][int(i)] for i in form.multicheck.data]
        print("chosen_lists:")
        print(chosen_lists) 
        generate_cl_pls(session["auth_head"], session["user_id"], chosen_lists)
        return redirect("/success")
    else:
        print(form.errors)

    return render_template('tracks.jinja2', form=form, track_names=session["track_names"], emojis=emojis)

@main_bp.route("/success", methods=['get'])
def success():
    return render_template('success.jinja2')

@main_bp.route("/deneme")
def deneme():
    return render_template("deneme.jinja2")

@main_bp.route("/temp")
def temp():
    return render_template("temp.jinja2")