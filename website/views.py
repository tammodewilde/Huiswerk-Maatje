import json
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
#from .models import Note
from . import db
import openai
import os

api_key = os.environ["OPENAI_API_KEY"]

views = Blueprint("views", __name__)

#Login niet required
@views.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", user=current_user)

@views.route("/writing", methods=["GET", "POST"])
def writing():
    if request.method == "GET":
        return render_template("writing.html", user=current_user)
    
    if request.method == "POST":
        onderwerp = request.form.get("onderwerp")
        lengte = request.form.get("lengte")
        tekstsoort = request.form.get("tekstsoort")
        schrijfdoel = request.form.get("schrijfdoel")
        #sleutelwoorden = [request.form.get("sw1"),request.form.get("sw2"),request.form.get("sw3")]
        
        #input checken op correcte invoer
        if not onderwerp or not lengte or not tekstsoort or not schrijfdoel:
            flash("Vul alstublieft alle velden correct in.", category="error")
            return render_template("writing.html", user=current_user)
        elif len(onderwerp) < 1 or len(onderwerp) > 100:
            flash("Onderwerp mag niet meer dan 100 letters zijn.", category="error")
            return render_template("writing.html", user=current_user)
        elif not lengte.isnumeric() or int(lengte) < 50 or int(lengte) > 500:
            flash("Aantal woorden moet tussen 50 en 500 zijn.", category="error") 
            return render_template("writing.html", user=current_user)
            #nog meer inputchecks maken
 
        #correcte invoer
        output = get_gpt3_response(("Schrijf een academische tekst met als doel {} over {}. Jouw antwoord moet ongeveer {} woorden lang zijn.".format(schrijfdoel, onderwerp, lengte)), 3*int(lengte)) # Het moet de volgende sleutelwoorden bevatten: {}, sleutelwoorden
        #output = "Koeien zijn gedomesticeerde dieren die worden gebruikt voor het produceren van melk, leer, vlees en andere producten. Ze worden al duizenden jaren gehouden, en hun wortels kunnen worden teruggevoerd tot de oudste landbouwpopulaties van vierduizend jaar geleden. Koeien hebben een veelzijdigheid aan verschillende soorten. De meest voorkomende soorten zijn holstein zwart-wit gestreepte, jersey bruine, angus zwarte, galloway bruin-zwart en lakenvelder kleurig. Ze kunnen worden ingedeeld in soorten als melkkoeien, vleescattle en huisfok. Koeien hebben een gemiddelde levensduur van tien tot veertien jaar, afhankelijk van hun behandelingsregime. Ze zijn intelligente wezens die in staat zijn om zich aan te passen aan hun omgeving, en ze hebben een gezamenlijke taal die wordt gebruikt om te communiceren met andere koeien. De melk die door koeien wordt geproduceerd, is het meest voorkomende product van koeien. Het is een goede bron van eiwitten, calcium en vitamine. Ook is het rijk aan verzadigde vetten en cholesterol, wat goed is voor de gezondheid van mensen. Koeien worden ook gebruikt voor het produceren van andere producten zoals leer en vlees. Koeien hebben veel verschillende verzorging nodig om gezond te blijven en productief te blijven. Ze hebben een verscheidenheid aan velden, schuilplaatsen en ruwvoer nodig. Voeding is cruciaal voor hun gezondheid, met name eiwitrijke diervoeding en ruwvoer. Koeien moeten ook regelmatig geïnspecteerd worden voor ziekte en parasieten. In het algemeen is het ras koeien een van de meest bruikbare en economisch rendabele vee in de moderne landbouw."

        return render_template("resultaat.html", user=current_user, output=output)


def get_gpt3_response(prompt, tokens):
    response = openai.Completion.create(
    engine="text-davinci-003",
    prompt=prompt,
    max_tokens=tokens,
    n = 1,
    temperature=0.8,
    )
    return response["choices"][0]["text"]





