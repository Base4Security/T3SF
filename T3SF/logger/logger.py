from T3SF.gui.core import MessageAnnouncer
from datetime import datetime
import json
import uuid


class T3SF_Logger:
    @staticmethod
    def emit(message,message_type="DEBUG"):
        try:
            message = message.replace("\n"," ")

            # Create a dictionary with the message data
            message_data = {
                "id" : str(uuid.uuid4()),
                "type" : message_type,
                "content": message,
                "timestamp": datetime.now().strftime("%H:%M:%S")
            }

            # Convert the dictionary to a JSON string
            sse_msg = f"data: {json.dumps(message_data)}\n\n"

            announcer = MessageAnnouncer()
            announcer.announce(msg=sse_msg)

            # Do something with the EventSource-formatted message, such as writing it to a file
            with open('logs.txt', 'a+') as f:
                f.write(sse_msg)

            # Print some critical information to the terminal
            if message_type in ['WARN', 'ERROR']:
                red = '\033[91m\033[5m'
                yellow = '\033[93m\033[5m'
                nc = '\033[0m'

                if message_type == "WARN":
                    text = yellow + "[!] " + nc + message
                else:
                    text = red + "[✗] " + nc + message
                print(text)

        except Exception as e:
            print(f"We could not print this message on the webpage:\n{message}")