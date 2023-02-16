# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import numpy as np 
import pandas as pd

import scholarly

class ProfessorCollaboratorsAction(Action):
    def name(self) -> Text:
        return "action_professor_collaborators"


    def get_professor_info(name):
            # look up professor by name
            professor = df.loc[df['Name'] == name]

            if professor.empty:
                # professor not found
                return {'error': 'Professor not found'}

            # extract information
            department = professor['Department'].iloc[0]
            office = professor['Office'].iloc[0]
            # add more fields as needed

            # return information as a dictionary
            return {'department': department, 'office': office}


    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        df = pd.read_csv('Data_Teachers.csv')
              

        # Get the professor's name from the user input
        professor_name = tracker.latest_message['entities'][0]['value']
        a = np.array((2))

        (b,c) = self.get_professor_info(professor_name)
        print("Hey, department is",b,"and office is", c)


        # Find the professor in the dataframe
        professor = df.loc[df['Name'] == professor_name]
        
        if len(professor) == 0:
            # If professor not found in the dataframe, return an error message
            dispatcher.utter_message(text=f"Sorry, I could not find any professor with the name {professor_name}.")
        else:
            # Retrieve the collaborators of the professor from Google Scholar
            search_query = scholarly.search_author(professor_name)
            author = next(search_query).fill()
            collaborators = [c.name for c in author.coauthors]
            
            # Find other professors in the dataframe and compare their collaborators with the selected professor's collaborators
            other_professors = df.loc[df['Name'] != professor_name]
            common_collaborators = set(collaborators)
            for index, row in other_professors.iterrows():
                search_query = scholarly.search_author(row['Name'])
                author = next(search_query).fill()
                other_collaborators = [c.name for c in author.coauthors]
                common_collaborators = common_collaborators.intersection(other_collaborators)
            
            # If there are common collaborators, return their names
            if len(common_collaborators) > 0:
                message = f"The common collaborators of {professor_name} with other professors are: "
                message += ', '.join(list(common_collaborators))
                dispatcher.utter_message(text=message)
            else:
                # If there are no common collaborators, return a message saying so
                dispatcher.utter_message(text=f"There are no common collaborators of {professor_name} with other professors.")
        
        return []
