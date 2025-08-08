import json
import os
import requests
import datetime
import time
from tabulate import tabulate # Used for pretty-printing tables

# --- Configuration ---
# IMPORTANT: Replace with your actual OpenAI API key or Google Cloud API key for Gemini.
# If using Google Gemini, you'll also need to adjust the API URL and model name below.
OPENAI_API_KEY = "" # Your provided key: sk-proj-XXyVVJ3XxnhHKeoMydMQp_jRRuHTrtLfDgbQdwXvioCn0c1Z4mZnY2wuJ12AnL00aKKtor-yVWFT3BlbkFJEB8072e6KUKtDMWeUX0svWGt2eVKdBlghNU8s-uMdvsXgRGPLUUpJ0BF6JCyyzuP6B4a-4pEIA

DATA_FILE = "destinations.json"

# --- 1. Destination Class ---
class Destination:
    """
    Represents a single travel destination with its details.
    """
    def __init__(self, city, country, start_date, end_date, budget, activities):
        self.city = city
        self.country = country
        self.start_date = start_date
        self.end_date = end_date
        self.budget = float(budget) # Ensure budget is stored as a float
        self.activities = activities # List of strings

    def update_details(self, new_city=None, new_country=None, new_start_date=None,
                       new_end_date=None, new_budget=None, new_activities=None):
        """
        Updates the details of the destination.
        Only updates fields that are not None.
        """
        if new_city: self.city = new_city
        if new_country: self.country = new_country
        if new_start_date: self.start_date = new_start_date
        if new_end_date: self.end_date = new_end_date
        if new_budget is not None: self.budget = float(new_budget)
        if new_activities: self.activities = new_activities
        print(f"Destination '{self.city}' updated successfully.")

    def __str__(self):
        """
        Returns a formatted string representation of the Destination object.
        """
        return (f"City: {self.city}, Country: {self.country}\n"
                f"Dates: {self.start_date} to {self.end_date}\n"
                f"Budget: ${self.budget:,.2f}\n"
                f"Activities: {', '.join(self.activities)}")

    def to_dict(self):
        """
        Converts the Destination object into a dictionary for JSON serialization.
        """
        return {
            "city": self.city,
            "country": self.country,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "budget": self.budget,
            "activities": self.activities
        }

    @staticmethod
    def from_dict(data):
        """
        Creates a Destination object from a dictionary (for JSON deserialization).
        """
        return Destination(
            data["city"],
            data["country"],
            data["start_date"],
            data["end_date"],
            data["budget"],
            data["activities"]
        )

# --- 2. AITravelAssistant Class ---
class AITravelAssistant:
    """
    Handles API calls to OpenAI (or compatible LLM) for generating travel assistance.
    """
    def __init__(self, api_key):
        self.api_key = api_key
        # Defaulting to OpenAI's Chat Completions API endpoint and model
        # If using Google's Gemini, change this URL and model name below.
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.model_name = "gpt-3.5-turbo" # Or "gemini-pro" / "gemini-2.5-flash-preview-05-20"
        
    def _make_api_call(self, prompt_text):
        """
        Internal method to make the API request with exponential backoff.
        """
        if not self.api_key:
            print("\nError: API key not set. Please set OPENAI_API_KEY to use AI features.")
            return "AI feature unavailable: API Key not configured."

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt_text}],
            "max_tokens": 700, # Increased max tokens for more detailed itineraries
            "temperature": 0.7 # Creativity level
        }

        retries = 0
        max_retries = 5
        while retries < max_retries:
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=45) # Increased timeout
                response.raise_for_status() # Raises HTTPError for bad responses (4xx or 5xx)
                response_data = response.json()
                if response_data and response_data.get('choices'):
                    return response_data['choices'][0]['message']['content'].strip()
                else:
                    return "AI did not return a valid response."
            except requests.exceptions.HTTPError as errh:
                print(f"HTTP Error: {errh}")
                if errh.response.status_code == 429: # Too Many Requests
                    retry_after = int(errh.response.headers.get("Retry-After", 1))
                    print(f"Rate limit exceeded. Retrying in {retry_after} seconds...")
                    time.sleep(retry_after + (2 ** retries)) # Add exponential backoff to Retry-After
                    retries += 1
                else:
                    print(f"Server responded with status code: {errh.response.status_code}")
                    return f"API Error: {errh.response.text}"
            except requests.exceptions.ConnectionError as errc:
                print(f"Error Connecting to API: {errc}")
                time.sleep(2 ** retries) # Exponential backoff
                retries += 1
            except requests.exceptions.Timeout as errt:
                print(f"Timeout Error: {errt}")
                time.sleep(2 ** retries) # Exponential backoff
                retries += 1
            except requests.exceptions.RequestException as err:
                print(f"An unexpected error occurred during API request: {err}")
                time.sleep(2 ** retries) # Exponential backoff
                retries += 1
            except json.JSONDecodeError as e:
                print(f"JSON decoding error: {e}. Response: {response.text}")
                return "AI response could not be parsed."

        print("Max retries reached. Could not complete API call.")
        return "AI feature unavailable after multiple retries."

    def generate_itinerary(self, destination):
        """
        Generates a daily travel itinerary for a given destination using the AI.
        """
        prompt = f"""
        Create a detailed, day-by-day travel itinerary for {destination.city}, {destination.country}
        from {destination.start_date} to {destination.end_date}.
        The estimated budget for this trip is ${destination.budget:,.2f} USD.
        Key activities the user is interested in include: {', '.join(destination.activities)}.
        Please include suggestions for morning, afternoon, and evening for each day,
        considering the budget and specified activities.
        """
        print(f"\nGenerating itinerary for {destination.city}...")
        return self._make_api_call(prompt)

    def generate_budget_tips(self, destination):
        """
        Generates budget-saving tips for a given destination using the AI.
        """
        prompt = f"""
        Provide 5-7 practical budget-saving tips for a trip to {destination.city}, {destination.country}
        with a budget of ${destination.budget:,.2f} USD, focusing on accommodation, food,
        transportation, and activities related to {', '.join(destination.activities)}.
        """
        print(f"\nGenerating budget tips for {destination.city}...")
        return self._make_api_call(prompt)

# --- 3. ItineraryManager Class ---
class ItineraryManager:
    """
    Manages a collection of Destination objects and handles file operations.
    """
    def __init__(self, ai_assistant):
        self.destinations = []
        self.ai_assistant = ai_assistant # Inject AI assistant
        self.load_from_file() # Load data when manager is initialized

    def add_destination(self):
        """
        Prompts user for destination details and adds a new Destination object.
        Includes input validation.
        """
        print("\n--- Add New Destination ---")
        city = input("Enter city: ").strip()
        country = input("Enter country: ").strip()

        # Check for duplicate city/country
        if any(d.city.lower() == city.lower() and d.country.lower() == country.lower() for d in self.destinations):
            print("Error: A destination with this city and country already exists.")
            return

        while True:
            start_date_str = input("Enter start date (YYYY-MM-DD): ").strip()
            if self._is_valid_date_format(start_date_str):
                break
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        while True:
            end_date_str = input("Enter end date (YYYY-MM-DD): ").strip()
            if self._is_valid_date_format(end_date_str) and start_date_str <= end_date_str:
                break
            else:
                print("Invalid date format or end date is before start date. Please use YYYY-MM-DD and ensure it's after or on the start date.")

        while True:
            try:
                budget = float(input("Enter budget (USD): ").strip())
                if budget > 0:
                    break
                else:
                    print("Budget must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number for budget.")

        activities_input = input("Enter activities (comma-separated): ").strip()
        # FIX: Removed the extra 'a' in 'for a a in'
        activities = [a.strip() for a in activities_input.split(',') if a.strip()]
        
        if not activities:
            print("Activities list cannot be empty. Please add at least one activity.")
            return

        new_destination = Destination(city, country, start_date_str, end_date_str, budget, activities)
        self.destinations.append(new_destination)
        print(f"Destination '{city}' added successfully!")
        self.save_to_file() # Save automatically after adding

    def remove_destination(self):
        """
        Removes a destination by city name.
        Handles non-existent destinations.
        """
        print("\n--- Remove Destination ---")
        city_to_remove = input("Enter the city of the destination to remove: ").strip()
        
        original_count = len(self.destinations)
        # Filter out the destination to be removed (case-insensitive)
        self.destinations = [d for d in self.destinations if d.city.lower() != city_to_remove.lower()]
        
        if len(self.destinations) < original_count:
            print(f"Destination '{city_to_remove}' removed successfully.")
            self.save_to_file() # Save automatically after removing
        else:
            print(f"Destination '{city_to_remove}' not found.")

    def update_destination(self):
        """
        Updates an existing destination's details.
        """
        print("\n--- Update Destination ---")
        city_to_update = input("Enter the city of the destination to update: ").strip()
        
        found_destination = None
        for d in self.destinations:
            if d.city.lower() == city_to_update.lower():
                found_destination = d
                break
        
        if not found_destination:
            print(f"Destination '{city_to_update}' not found.")
            return

        print(f"Current details for {found_destination.city}:\n{found_destination}")
        print("\nEnter new values (leave blank to keep current value):")

        new_city = input(f"New City ({found_destination.city}): ").strip() or None
        new_country = input(f"New Country ({found_destination.country}): ").strip() or None
        
        new_start_date = None
        while True:
            date_input = input(f"New Start Date ({found_destination.start_date}) (YYYY-MM-DD): ").strip()
            if not date_input:
                break
            if self._is_valid_date_format(date_input):
                new_start_date = date_input
                break
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")

        new_end_date = None
        while True:
            date_input = input(f"New End Date ({found_destination.end_date}) (YYYY-MM-DD): ").strip()
            if not date_input:
                break
            if self._is_valid_date_format(date_input):
                if new_start_date and date_input < new_start_date:
                    print("End date cannot be before new start date. Please re-enter.")
                elif not new_start_date and date_input < found_destination.start_date:
                    print("End date cannot be before current start date. Please re-enter.")
                else:
                    new_end_date = date_input
                    break
            else:
                print("Invalid date format. Please use YYYY-MM-DD.")
        
        new_budget = None
        while True:
            budget_input = input(f"New Budget ({found_destination.budget:,.2f} USD) (leave blank to keep): ").strip()
            if not budget_input:
                break
            try:
                temp_budget = float(budget_input)
                if temp_budget > 0:
                    new_budget = temp_budget
                    break
                else:
                    print("Budget must be a positive number.")
            except ValueError:
                print("Invalid input. Please enter a number for budget.")

        activities_input = input(f"New Activities (comma-separated, current: {', '.join(found_destination.activities)}) (leave blank to keep): ").strip()
        new_activities = [a.strip() for a in activities_input.split(',') if a.strip()] if activities_input else None
        if new_activities is not None and not new_activities: # If user entered empty string, and it became an empty list, keep old
             new_activities = found_destination.activities


        found_destination.update_details(new_city, new_country, new_start_date,
                                        new_end_date, new_budget, new_activities)
        self.save_to_file() # Save automatically after updating

    def view_all_destinations(self, sorted_by=None):
        """
        Displays all destinations in a clean tabular format.
        Optional: sort by 'start_date' or 'budget'.
        """
        if not self.destinations:
            print("\nNo destinations added yet.")
            return

        headers = ["City", "Country", "Start Date", "End Date", "Budget (USD)", "Activities"]
        table_data = []

        # Create a copy to sort, so the original list order isn't changed permanently unless saved
        display_destinations = list(self.destinations)

        if sorted_by == 'start_date':
            display_destinations.sort(key=lambda d: datetime.datetime.strptime(d.start_date, '%Y-%m-%d'))
            print("\n--- All Destinations (Sorted by Start Date) ---")
        elif sorted_by == 'budget':
            display_destinations.sort(key=lambda d: d.budget)
            print("\n--- All Destinations (Sorted by Budget) ---")
        else:
            print("\n--- All Destinations ---")

        for dest in display_destinations:
            table_data.append([
                dest.city,
                dest.country,
                dest.start_date,
                dest.end_date,
                f"{dest.budget:,.2f}",
                ", ".join(dest.activities)
            ])
        
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def search_destination(self):
        """
        Searches for destinations by city, country, or keyword in activities.
        """
        print("\n--- Search Destination ---")
        query = input("Enter city, country, or keyword for activities to search: ").strip().lower()
        
        found_results = []
        for d in self.destinations:
            if (query in d.city.lower() or
                query in d.country.lower() or
                any(query in a.lower() for a in d.activities)):
                found_results.append(d)
        
        if found_results:
            print("\n--- Search Results ---")
            headers = ["City", "Country", "Start Date", "End Date", "Budget (USD)", "Activities"]
            table_data = []
            for dest in found_results:
                table_data.append([
                    dest.city,
                    dest.country,
                    dest.start_date,
                    dest.end_date,
                    f"{dest.budget:,.2f}",
                    ", ".join(dest.activities)
                ])
            print(tabulate(table_data, headers=headers, tablefmt="grid"))
        else:
            print(f"No destinations found matching '{query}'.")

    def save_to_file(self):
        """
        Saves all destinations to a JSON file.
        """
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump([d.to_dict() for d in self.destinations], f, indent=4)
            print(f"\nItinerary saved to '{DATA_FILE}'.")
        except IOError as e:
            print(f"Error saving itinerary to file: {e}")

    def load_from_file(self):
        """
        Loads destinations from a JSON file when the program starts.
        """
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
                    self.destinations = [Destination.from_dict(d) for d in data]
                print(f"\nItinerary loaded from '{DATA_FILE}'.")
            except json.JSONDecodeError as e:
                print(f"Error loading itinerary: Invalid JSON format in '{DATA_FILE}'. Details: {e}")
                self.destinations = [] # Clear corrupted data
            except IOError as e:
                print(f"Error loading itinerary from file: {e}")
            except Exception as e:
                print(f"An unexpected error occurred during load: {e}")
        else:
            print(f"\n'{DATA_FILE}' not found. Starting with an empty itinerary.")

    def _is_valid_date_format(self, date_str):
        """Helper to validate YYYY-MM-DD date format."""
        try:
            datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return True
        except ValueError:
            return False

    def ai_assistance_menu(self):
        """
        Sub-menu for AI Travel Assistance features.
        """
        print("\n--- AI Travel Assistance ---")
        if not self.destinations:
            print("Please add destinations first to use AI assistance.")
            return

        # Let user select a destination for AI assistance
        print("\nSelect a destination for AI assistance:")
        headers = ["#", "City", "Country"]
        table_data = []
        for i, dest in enumerate(self.destinations):
            table_data.append([i + 1, dest.city, dest.country])
        print(tabulate(table_data, headers=headers, tablefmt="grid"))

        while True:
            try:
                choice = int(input("Enter the number of the destination (0 to cancel): ").strip())
                if choice == 0:
                    return
                if 1 <= choice <= len(self.destinations):
                    selected_destination = self.destinations[choice - 1]
                    break
                else:
                    print("Invalid number. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        while True:
            print(f"\nAI Assistance for {selected_destination.city}, {selected_destination.country}:")
            print("1. Generate Daily Itinerary")
            print("2. Get Budget Saving Tips")
            print("3. Back to Main Menu")
            ai_choice = input("Enter your choice: ").strip()

            if ai_choice == '1':
                itinerary_response = self.ai_assistant.generate_itinerary(selected_destination)
                print("\n--- AI Generated Itinerary ---")
                print(itinerary_response)
            elif ai_choice == '2':
                tips_response = self.ai_assistant.generate_budget_tips(selected_destination)
                print("\n--- AI Generated Budget Tips ---")
                print(tips_response)
            elif ai_choice == '3':
                break
            else:
                print("Invalid choice. Please select 1, 2, or 3.")


# --- Main Application Logic ---
def display_menu():
    """Displays the main menu options."""
    print("\n--- Travel Itinerary Planner Menu ---")
    print("1. Add Destination")
    print("2. Remove Destination")
    print("3. Update Destination")
    print("4. View All Destinations")
    print("5. Search Destination")
    print("6. AI Travel Assistance")
    print("7. Sort Destinations (Bonus)")
    print("8. Save Itinerary")
    print("9. Load Itinerary") # This is automatically done on startup, but kept for explicit action
    print("0. Exit")
    print("------------------------------------")

def main():
    """Main function to run the Travel Itinerary Planner."""
    ai_assistant = AITravelAssistant(OPENAI_API_KEY)
    manager = ItineraryManager(ai_assistant)

    while True:
        display_menu()
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            manager.add_destination()
        elif choice == '2':
            manager.remove_destination()
        elif choice == '3':
            manager.update_destination()
        elif choice == '4':
            manager.view_all_destinations()
        elif choice == '5':
            manager.search_destination()
        elif choice == '6':
            manager.ai_assistance_menu()
        elif choice == '7':
            print("\n--- Sort Destinations ---")
            sort_option = input("Sort by (start_date/budget/none): ").strip().lower()
            if sort_option in ['start_date', 'budget']:
                manager.view_all_destinations(sorted_by=sort_option)
            else:
                print("Invalid sort option. Displaying without sorting.")
                manager.view_all_destinations()
        elif choice == '8':
            manager.save_to_file()
        elif choice == '9':
            manager.load_from_file() # Explicit load
        elif choice == '0':
            print("\nExiting Travel Itinerary Planner. Goodbye!")
            manager.save_to_file() # Ensure data is saved on exit
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()