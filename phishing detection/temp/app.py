import numpy as np
from flask import Flask, app, request, render_template
from keras.models import load_model
import requests

import ageofdomain, double_slash_redirecting , favicon , googleindex , having_at_symbol , having_IP, having_subdomain , https_token , iframe , links_in_tags , onmouseover , pagerank , popupwindow , prefix_suffx , redirect , rightclick , sfh , shortening_service , submitting_to_email , URL_Length , url_of_anchor

l = [ageofdomain.determine_legitimacy , double_slash_redirecting.detect_double_slash , favicon.is_phishing , googleindex.determine_legitimacy , having_at_symbol.detect_at_symbol , having_IP.detect_ip_in_url, having_subdomain.detect_url_category , https_token.check_url , iframe.determine_legitimacy , links_in_tags.analyze_website , onmouseover.check_website_legitimacy , pagerank.check_website_legitimacy , popupwindow.check_website_legitimacy , prefix_suffx.detect_prefix_suffix , redirect.check_website_legitimacy , rightclick.detect_right_click_disabled , sfh.determine_website_status , shortening_service.shortening_service , submitting_to_email.mails , URL_Length.classify_url , url_of_anchor.check_anchor_tags]

model = load_model(r"Phising.h5",compile=False)
app=Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form["url"]

        try:
            # Fetch the webpage
            response = requests.get(url)
            if response.status_code != 200:
                return render_template("prediction.html",url=url, error="Error fetching webpage: {} {}".format(response.status_code, response.reason))

            features = [func(url) for func in l]

            input_data = np.array(features).reshape(1, -1)

            prediction = model.predict(input_data)

            prediction_result = round(prediction[0][0])
            if not prediction_result:
                result_text = "Phishing"
            else:
                result_text = "Legitimate"

            return render_template("prediction.html", url=url, prediction=result_text)

        except requests.exceptions.RequestException as e:
            return render_template("prediction.html", error=str(e))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)