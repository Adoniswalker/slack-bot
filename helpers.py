from flask import make_response

import bot
from spaces import GoogleSheet

pyBot = bot.Bot()


def get_centers(centers):
    return [{"name": "center", "text": i, "type": "button", "value": i} for i in centers]


def response_message(user, andela_centers):
    centers = get_centers(andela_centers)
    cancel_btn = {"name": "center", "text": "Cancel", "type": "button", "value": "cancel", "style": "danger"}
    centers.append(cancel_btn)
    return {
        "text": "Welcome <@{0}>. Which center would you like to interact with?".format(user),
        "attachments": [
            {
                "text": "Choose a center to book",
                "fallback": "You are unable to choose a center",
                "callback_id": "center_choosing",
                "color": "#0080ff",
                "attachment_type": "default",
                "actions": centers
            }
        ]
    }


def sits_attachment():
    data_sheet = GoogleSheet()
    hot_desk = data_sheet.get_all_hot_desks()
    hot_desk_actions = [
        {"name": "hot_desk", "text": "{} {} {} {}".format(i[0], i[1], i[2], [3]), "type": "button", "value": i,
         "style": "primary"} for i
        in
        hot_desk]
    return {
        "text": "Choose a sit locations",
        "fallback": "You are unable to choose a sit",
        "callback_id": "sit_choosing",
        "color": " #cc0066",
        "attachment_type": "default",
        "actions": hot_desk_actions
    }


def authenticate_slack(token):
    if pyBot.verification != token:
        message = "Invalid Slack verification token: %s \npyBot has: \
                       %s\n\n" % (token, pyBot.verification)
        # By adding "X-Slack-No-Retry" : 1 to our response headers, we turn off
        # Slack's automatic retries during development.
        make_response(message, 403, {"X-Slack-No-Retry": 1})
    return True


def unavailable_response():
    return {
        "title": "Unavailable",
        "text": "At the moment, this feature is only available to Other Andela centers"
    }
