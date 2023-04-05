from difflib import SequenceMatcher
from collections import Counter
import random
import json
import re 

class Slack(object):
        def __init__(self, app):
            self.app = app

        def regex_finder(self, input):
            """
            Matches repeated words counting the 
            amount of times the word is being repeated.
            """
            words = input.split('-')
            dict = Counter(words)
            for key in words:
                if dict[key]>1:
                    return key
            return False

        def Formatter(self=None, title=None, description=None, color="CYAN", image=None, author=None, buttons=None, text_input=None, checkboxes=None):
            colors = {'BLUE' : '#428bca', 'RED' : '#d9534f', 'WHITE' : '#f9f9f9', 'CYAN' : '#5bc0de', 'GREEN' : '#5cb85c', 'ORANGE' : '#ffa700', 'YELLOW' : '#ffff00'}

            fallback_text = ""
            color = colors[color]
            result =[
                        {
                            "color": color,
                            "blocks": []
                        }
                    ]

            if title != None:
                title_list = [
                                {
                                    "type": "header",
                                    "text": {
                                        "type": "plain_text",
                                        "text": title
                                    }
                                },
                                {
                                    "type": "divider"
                                }
                            ]

                result[0]["blocks"] = title_list

            if description != None:
                desc_list = {
                                "type": "section",
                                "text": {
                                    "type": "mrkdwn",
                                    "text": description
                                }
                            }
                result[0]["blocks"].append(desc_list)

            else:
                description = "Preview not available."
                desc_list = {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": description
                    }
                }
                result[0]["blocks"].append(desc_list)

            if image != None:
                fallback_text = "🖼 "
                image_list = {
                                "type": "image",
                                "title": {
                                    "type": "plain_text",
                                    "text": image["name"],
                                    "emoji": True
                                },
                                "image_url": image["image_url"],
                                "alt_text": "image"
                            }
                result[0]["blocks"].append(image_list)

            if author != None:
                author_list = [{
                                "type": "context",
                                "elements": [
                                    {
                                        "type": "image",
                                        "image_url": author["image_url"],
                                        "alt_text": author["name"]
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": author["name"],
                                    },
                                    {
                                        "type": "mrkdwn",
                                        "text": " |  *" + author["date"] + "*",
                                    }
                                ]
                              }]
                result[0]["blocks"][1:1] = author_list

            if text_input != None:
                input_list = {
                                "block_id": "input_texto",
                                "dispatch_action": text_input['dispatch_action'],
                                "type": "input",
                                "element": {
                                    "type": "plain_text_input",
                                    "action_id": text_input["action_id"]
                                },
                                "label": {
                                    "type": "plain_text",
                                    "text": text_input["label"]
                                }
                            }
                result[0]["blocks"].append(input_list)

            if checkboxes != None:
                chk_boxes_list = {
                    "block_id": "checkboxes",
                    "type": "input",
                    "label": {
                        "type": "plain_text",
                        "text": checkboxes['title'],
                        "emoji": True
                    },
                    "element": {
                        "type": "checkboxes",
                        "options": []
                    }
                }
                if 'action_id' in checkboxes:
                    chk_boxes_list['element']["action_id"] = checkboxes['action_id']

                for checkbox in checkboxes['checkboxes']:
                    boxes_list = {
                                "text": {
                                    "type": "plain_text",
                                    "text": checkbox['text'],
                                    "emoji": True
                                },
                                "value": checkbox['value']
                                }
                    chk_boxes_list['element']['options'].append(boxes_list)

                result[0]["blocks"].append(chk_boxes_list)

            if buttons != None:
                actions_list = {
                                "type": "actions",
                                "elements": []
                               }
                
                for button in buttons:
                    button_list = {
                                    "type": "button",
                                    "text": {
                                        "type": "plain_text",
                                        "text": button['text']
                                    },
                                    "style": button['style'],
                                    "value": button['value'],
                                    "action_id": button['action_id']
                                    }
                    actions_list['elements'].append(button_list)

                result[0]["blocks"].append(actions_list)

            result[0]["fallback"] = (fallback_text + description)

            return result

        async def InboxesAuto(self, T3SF_instance, regex=None):
            if regex != None:
                mensaje_inboxes = ""
                for player in T3SF_instance.players_list:
                    for channel in T3SF_instance.ch_names_list:
                        if regex in channel:
                            accuracy = similar(re.sub(f"({regex})", "", str(channel)).lower(), str(player).lower().replace(" ", "-"))
                            if accuracy >= 0.4:
                                T3SF_instance.inboxes_all[player] = channel
                        
                json.dump(T3SF_instance.inboxes_all,open(f"inboxes_{T3SF_instance.platform}.json", "w"))

                for player in T3SF_instance.inboxes_all:
                    mensaje_inboxes += f"Inbox {player} [{T3SF_instance.inboxes_all[player]}]\n"

                T3SF_instance.response_auto = await self.EditMessage(response=T3SF_instance.response_auto, color="YELLOW", title = f"📩 Inboxes fetched! [{len(T3SF_instance.inboxes_all)}]", description=mensaje_inboxes)
                
                T3SF_instance.regex_ready = True

            elif T3SF_instance.fetch_inboxes == True:

                T3SF_instance.response_auto = await self.SendMessage(channel = T3SF_instance._ctx['channel'], color="CYAN", title="💬 Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!")

                channels = await T3SF_instance.app.client.conversations_list(types="public_channel,private_channel")

                for channel in channels['channels']:
                    T3SF_instance.ch_names_list.append(channel['name'])

                channels_itinerator = 0
                regex = ""
                past_channel = None

                while regex == "":
                    for channel in T3SF_instance.ch_names_list:
                        if channels_itinerator == 0 and channel == past_channel:
                            past_channel = channel
                            channels_itinerator += 1
                            continue
                        
                        match_channel = self.regex_finder(str(channel).lower() + "-" + str(past_channel).lower())

                        if match_channel != False:
                            for character in past_channel:
                                if character in channel:
                                    regex += character
                                else:
                                    break
                            break
                        else:
                            channels_itinerator += 1
                            past_channel = channel
                            continue

                image = {"image_url":"https://i.ibb.co/34rTqMH/image.png", "name": "regex"}
                buttons = [{"text":"Yes!", "style": "primary", "value": regex, "action_id": "regex_yes"},{"text":"No.", "style": "danger", "value": "click_me_456", "action_id": "regex_no"}]
                
                T3SF_instance.response_auto = await self.EditMessage(response=T3SF_instance.response_auto, color="GREEN", title = "ℹ️ Regex detected!", description = f"Please confirm if the regex detected for the channels, is correct so we can get the inboxes!\n\nExample:\ninbox-legal\nThe regex should be `inbox-`\n\n*Detected regex:* `{regex}`\n\n\nPlease select your answer below.", image=image, buttons = buttons)
                T3SF_instance.regex_ready = False

            else:
                mensaje_inboxes = ""
                T3SF_instance.response_auto = await self.SendMessage(channel = T3SF_instance._ctx['channel'], color="CYAN", title="💬 Fetching inboxes...", description=f"Please wait while we fetch all the inboxes in this server!")

                for player in T3SF_instance.inboxes_all:
                    mensaje_inboxes += f"Inbox {player} [{T3SF_instance.inboxes_all[player]}]\n"

                T3SF_instance.response_auto = await self.EditMessage(response=T3SF_instance.response_auto, color="YELLOW", title = f"📩 Inboxes fetched! [{len(T3SF_instance.inboxes_all)}]", description=mensaje_inboxes)

                T3SF_instance.regex_ready = True

        async def InjectHandler(self, T3SF_instance):
            image = None

            author = {"name": T3SF_instance._inject["From"], "date": T3SF_instance._inject["Date"]}

            player = T3SF_instance._inject['Player']

            if "Photo" in T3SF_instance._inject and T3SF_instance._inject['Photo'] != '':
                if "Picture Name" in T3SF_instance._inject and T3SF_instance._inject['Picture Name'] == '' or "Photo" not in T3SF_instance._inject:
                    attachment_name = "attachment.jpg"
                else:
                    attachment_name = T3SF_instance._inject['Picture Name']
                image = {"name": attachment_name, "image_url": T3SF_instance._inject['Photo']}
            
            if "Profile" in T3SF_instance._inject and T3SF_instance._inject['Profile'] != '':
                author["image_url"] = T3SF_instance._inject['Profile']
                
            else:
                profile_pic = random.choice([
                    "https://ssl.gstatic.com/ui/v1/icons/mail/profile_mask2.png",
                    "https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAAAAAA/4252rscbv5M/photo.jpg",
                    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSTt8Dg9RL4IGOjsJ2Fr-lXThf-DGM5YgPB6j5rD8tHQ9RLrU-03H4dYeskL01FNajqL_0&usqp=CAU"
                ])
                author["image_url"] = profile_pic
            
            await self.SendMessage(channel = T3SF_instance.inboxes_all[player], title=T3SF_instance._inject['Subject'], description=T3SF_instance._inject["Script"], image=image, author=author, color="CYAN")

            return True

        async def PollHandler(self, T3SF_instance):
            T3SF_instance.poll_answered = False
            
            image = None

            player = T3SF_instance._inject['Player']

            if "Photo" in T3SF_instance._inject and T3SF_instance._inject['Photo'] != '':
                if "Picture Name" in T3SF_instance._inject and T3SF_instance._inject['Picture Name'] == '' or "Photo" not in T3SF_instance._inject:
                    attachment_name = "attachment.jpg"
                else:
                    attachment_name = T3SF_instance._inject['Picture Name']
                image = {"name": attachment_name, "image_url": T3SF_instance._inject['Photo']}

            poll_options = T3SF_instance._inject['Poll'].split('|')
            
            actual_real_time = re.sub("([^0-9])", "", T3SF_instance._inject['Real Time'])[-2:]
            
            next_real_time = re.sub("([^0-9])", "", T3SF_instance.data[int(T3SF_instance._inject['#'])]['Real Time'])[-2:]

            diff = int(next_real_time) - int(actual_real_time)
            if diff < 0:
                diff_no_real = int(actual_real_time) - int(next_real_time)
                diff = 60 - diff_no_real 

            diff_secs = diff * 60

            description = T3SF_instance._inject["Script"] + f"\n\nYou have {diff} minute(s) to answer this poll!"

            buttons = [{"text": poll_options[0], "style": "primary", "value": 'option1', "action_id": "option1"},{"text":poll_options[1], "style": "primary", "value": "option2","action_id": "option2"}]

            T3SF_instance.response_poll = await self.SendMessage(channel = T3SF_instance.inboxes_all[player], title=T3SF_instance._inject['Subject'], description=description, image=image, buttons=buttons, color="YELLOW")

            return True

        async def PollAnswerHandler(self, T3SF_instance, body=None, payload=None):
            poll_msg = body['message']['attachments'][0]['fallback']
            poll_msg = poll_msg[: poll_msg.rfind('\n')]
            action_user = body['user']['username']
            selected_option = payload['text']['text']
            description = f'{poll_msg}\n\n@{action_user} selected: {selected_option}'

            T3SF_instance.poll_answered = True
            T3SF_instance.response_poll = await self.EditMessage(color = "GREEN", title="Poll Answered!", description=description, response=T3SF_instance.response_poll)
            await T3SF_instance.NotifyGameMasters(type_info="poll_answered", data={'msg_poll':poll_msg,'answer':selected_option,'user':action_user})
            return True

        async def SendMessage(self, T3SF_instance=None, color=None, title=None, description:str=None, channel=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None):
            if channel == None:
                channel = self._ctx['channel']

            try:
                attachments = self.Formatter(title=title, description=description, color=color, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes)
                self.response = await self.app.client.chat_postMessage(channel = channel, attachments = attachments)
                return self.response

            except Exception as e:
                raise

        async def EditMessage(self, T3SF_instance=None, color=None, title:str=None, description:str=None, response=None, image=None, author=None, buttons=None, text_input=None, checkboxes=None):
            self.response = await self.app.client.chat_update(channel=response['channel'], ts=response['ts'], attachments = self.Formatter(title=title, description=description, color=color, image=image, author=author, buttons=buttons, text_input=text_input, checkboxes=checkboxes))
            return self.response


def similar(a, b):
    """
    Based in graphics, find the similarity between 2 strings.
    """
    return SequenceMatcher(None, a, b).ratio()