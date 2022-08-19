from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from functools import wraps
import time as time
import datetime as dt
import traceback
import sys
from os import environ

def notify_me_noddy(app_name, user_id):

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.time()
            #Execute Function
            try:
                output = func(*args, **kwargs)

                # Get time in seconds
                elapsed = round((time.time() - start_time),3)
                notify(
                    [
                        {
                            "type": "header",
                            "text": {
                            "type": "plain_text",
                            "text": "Notification from Noddy!",
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": ':02_cheer: *App Completed Successfully!*'
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "fields":[
                               {
                                "type": "mrkdwn",
                                "text": ":robot_face:  *App Name:*"
                               },
                               {
                                "type": "mrkdwn",
                                "text": "*:clock1:  Time Finished:*"
                               },
                               {
                                "type": "mrkdwn",
                                "text": f"{app_name}"
                               },
                               {
                                "type": "mrkdwn",
                                "text": f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                               },
                               {
                                "type": "mrkdwn",
                                "text": ":residentsleeper: *Elapsed Time:*"
                               },
                               {
                                "type": "mrkdwn",
                                "text": " "
                               },
                               {
                                "type": "mrkdwn",
                                "text": f"{elapsed} seconds"
                               },
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f'*Output*: \n```{output}```'
                            }
                        }
                    ],
                    user_id
                )

            except Exception as e:
                notify(
                    [
                        {
                            "type": "header",
                            "text": {
                            "type": "plain_text",
                            "text": "Notification from Noddy!",
                            }
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f':sadge: *Something Broke.*'
                            }
                        },
                        {
                            "type": "divider"
                        },
                        {
                            "type": "section",
                            "fields":[
                               {
                                "type": "mrkdwn",
                                "text": ":robot_face:  *App Name:*"
                               },
                               {
                                "type": "mrkdwn",
                                "text": "*:clock1:  Time Failed:*"
                               },
                               {
                                "type": "mrkdwn",
                                "text": f"{app_name}"
                               },
                               {
                                "type": "mrkdwn",
                                "text": f"{dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                               },
                            ]
                        },
                        {
                            "type": "section",
                            "text": {
                                "type": "mrkdwn",
                                "text": f'*Stack Trace*: \n```{traceback.format_exc()}```'
                            }
                        }
                    ],
                    user_id
                )
                raise e
            {traceback.format_exc()}

            return output

        def notify(block, user_id):

            bot_token = environ['BOT_TOKEN']
            client = WebClient(bot_token)
            try:
                response = client.chat_postEphemeral(
                    user = user_id,
                    blocks = block,
                    channel = environ['channel']
                )
            except SlackApiError as e:
                assert e.response["error"]

        return wrapper
    return decorator

