# -*- coding: utf-8 -*-
"""
A routing layer for the onboarding bot tutorial built using
[Slack's Events API](https://api.slack.com/events-api) in Python
"""
import json
import os

from flask import Flask, request, make_response, jsonify
from slackclient import SlackClient

import bot
from helpers import response_message, sits_attachment, authenticate_slack, unavailable_response

pyBot = bot.Bot()
slack = pyBot.client
slack_bot = SlackClient(os.environ.get("SLACK_TOKEN"))

app = Flask(__name__)
andela_centers = ["Andela Lagos", "Andela Kenya", "Andela Rwanda"]


@app.route("/hotdesk", methods=["GET", "POST"])
def bot_desk():
    slack_data = request.values
    # ============== Slack challenge ====================#
    if "challenge" in slack_data:
        return make_response(slack_data["challenge"], 200, {"content_type":
                                                                "application/json"
                                                            })

    # ============ Slack Token Verification =========== #
    authenticate_slack(slack_data["token"])
    user = slack_data["user_id"]
    centers = response_message(user, andela_centers)
    return jsonify(centers)


@app.route("/listener", methods=["get", "POST"])
def listener():
    # get the interactive message
    slack_req = json.loads(request.form.get('payload'))
    # authenticate that the response is realy coming from slack
    authenticate_slack(slack_req["token"])
    if slack_req["actions"][0]["type"] == "button" and slack_req["actions"][0]["name"] == "center":
        # center has been chosen
        centers = response_message(slack_req["user"]["id"], andela_centers)
        if slack_req["actions"][0]["value"] == "Andela Lagos":
            # Andela lagos
            hot_dest_attachment = sits_attachment()
            centers["attachments"].append(hot_dest_attachment)
            return jsonify(centers)
        elif slack_req["actions"][0]["value"] == "cancel":
            return jsonify({"text": "Cancelled"})
        else:
            print("other compuses")
            centers["attachments"].append(unavailable_response())
            return jsonify(centers)

    elif slack_req["actions"][0]["type"] == "button" and slack_req["actions"][0]["name"] == "hot_desk":
        # a sit has been chosen
        user = slack_bot.api_call(
            "users.info",
            user=slack_req["user"]["id"]
        )
        print(user)
        response_data = {
            "title": "Request Submitted",
            "text": "You were able to submit"
        }
        return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
