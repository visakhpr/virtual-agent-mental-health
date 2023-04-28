import sqlite3
import os
import json
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher
from datetime import datetime
from rasa_sdk.types import DomainDict


class SaveSlotValues(Action):
    def name(self) -> Text:
        return "action_save_slot_values"

    def run(
        self, 
        dispatcher: CollectingDispatcher, 
        tracker: Tracker, 
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("name")
        mobile_number = tracker.get_slot("mobile_number")
        email_address = tracker.get_slot("email_address")
        age = tracker.get_slot("age")
        gender = tracker.get_slot("gender")
        marital_status = tracker.get_slot("marital_status")
        education = tracker.get_slot("education")
        district = tracker.get_slot("district")
        job_title = tracker.get_slot("job_title")

        # Save the path of chat history to the chat_history column of SQLite3 database
        dir_name = "qa_json_files"
        file_name = f"{user_name}_{mobile_number}.json"
        chat_history_path = os.path.join(dir_name, file_name)
        # Create a file name with the user's name and mobile number

        # Connect to the SQLite3 database
        conn = sqlite3.connect('user_database.db')
        
        # Create a cursor object
        cursor = conn.cursor()
        
        # Create the table if it does not exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users
            (
                name TEXT,
                mobile_number TEXT,
                email_address TEXT,
                age TEXT,
                gender TEXT,
                marital_status TEXT,
                education TEXT,
                district TEXT,
                job_title TEXT,
                chat_history TEXT
            )
        ''')
        
        # Insert the slot values into the database
        cursor.execute('''
            INSERT INTO users
            (
                name, mobile_number, email_address, age, gender, marital_status, education, district, job_title, chat_history
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_name, mobile_number, email_address, age, gender, marital_status, education, district, job_title, chat_history_path))
        
        # Commit the changes
        conn.commit()
        
        # Close the connection
        conn.close()
        
        # Set the slots
        slot_values = {
            "name": user_name,
            "mobile_number": mobile_number,
            "email_address": email_address,
            "age": age,
            "gender": gender,
            "marital_status": marital_status,
            "education": education,
            "district": district,
            "job_title": job_title,
        }
        
        return [SlotSet(slot_name, slot_value) for slot_name, slot_value in slot_values.items()]

class SaveQA(Action):
    def name(self) -> Text:
        return "action_save_qa"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> List[Dict[Text, Any]]:
        # Extract the last user message and the bot's response from the tracker events
        user_utterances = [event for event in tracker.events if event["event"] == "user" and "text" in event]
        last_user_utterance = user_utterances[-1]["text"] if user_utterances else None
        bot_utterances = [event for event in tracker.events if event["event"] == "bot" and "text" in event]
        last_bot_utterance = bot_utterances[-1]["text"] if bot_utterances else None

        # Extract the user's name and mobile number
        user_name = tracker.get_slot("name")
        mobile_number = tracker.get_slot("mobile_number")

        # Create a directory to save the QA JSON files
        dir_name = "qa_json_files"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)

        # Create a file name with the user's name and mobile number
        file_name = f"{user_name}_{mobile_number}.json"
        file_path = os.path.join(dir_name, file_name)

        # Create a dictionary with the QA pair
        qa_dict = {
            "Question": last_bot_utterance,
            "Answer": last_user_utterance
        }

        # Write the QA dictionary to a JSON file
        with open(file_path, "a") as file:
            json.dump(qa_dict, file, indent=4)

        return []





"""class ExtractKeywords(Action):

    def name(self) -> Text:
        return "action_extract_keywords"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("name")
        mobile_number = tracker.get_slot("mobile_number")

        # Read the text file
        with open(f"{user_name}_{mobile_number}_{datetime.now().strftime('%Y-%m-%d')}.txt", 'r') as f:
            content = f.read()

        # Extract the keywords using regular expressions
        keywords = {}
        keywords['email_address'] = re.findall(r'email_address:\s*(\S+)', content)[0]
        keywords['mobile_number'] = re.findall(r'mobile_number:\s*(\S+)', content)[0]
        keywords['name'] = re.findall(r'name:\s*(\S+)', content)[0]
        keywords['age'] = re.findall(r'age:\s*(\S+)', content)[0]
        keywords['gender'] = re.findall(r'gender:\s*(\S+)', content)[0]
        keywords['marital_status'] = re.findall(r'marital_status:\s*(\S+)', content)[0]
        keywords['education'] = re.findall(r'education:\s*(\S+)', content)[0]
        keywords['district'] = re.findall(r'district:\s*(\S+)', content)[0]
        keywords['job_title'] = re.findall(r'job_title:\s*(\S+)', content)[0]

        questions = re.findall(r'Question: (.+)\nAnswer: (.+)', content)
        for q, a in questions:
            if '/affirm' in a:
                keywords[q.replace(' ', '_')] = 'Yes'
            elif '/deny' in a:
                keywords[q.replace(' ', '_')] = 'No'
            elif '/right_response' in a:
                keywords[q.replace(' ', '_')] = 'Right response'
            elif '/deny_Cage' in a:
                keywords[q.replace(' ', '_')] = 'No, not applicable'
            elif '/affirm_Cage' in a:
                keywords[q.replace(' ', '_')] = 'Yes, guilty'

        # Print the extracted keywords
        print(keywords)

        return []"""
