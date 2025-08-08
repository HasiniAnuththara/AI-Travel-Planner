# ✈️ AI Travel Itinerary Planner

## Project Overview

The **AI Travel Itinerary Planner** is a command-line application built with Python that serves as a smart travel companion. It allows users to **manage their travel destinations** (add, remove, update, view, search) and leverages **Artificial Intelligence (AI)** through OpenAI (or Google Gemini) Chat Completions to generate personalized daily travel itineraries and budget-saving tips. This project demonstrates strong skills in Object-Oriented Programming (OOP), data persistence (JSON file handling), and API integration.

---

## ✨ Features

* **Add Destinations:** Create `Destination` objects with details like city, country, travel dates, budget, and a list of activities.
* **Remove Destinations:** Easily remove destinations by specifying the city name.
* **Update Destinations:** Modify any detail of an existing destination.
* **View All Destinations:** Display all saved destinations in a clear, tabular format.
* **Search Destinations:** Find specific trips by city, country, or keywords in activities.
* **Save Itinerary:** Persist all destination data to a `destinations.json` file.
* **Load Itinerary:** Automatically load saved destinations upon application startup.
* **AI Travel Assistance:**
    * **Generate Daily Itinerary:** Get a detailed day-by-day travel plan for a selected destination, customized by dates, budget, and activities.
    * **Generate Budget Tips:** Receive practical advice on saving money for your trip.
* **Data Validation:** Ensures correct input formats for dates and positive numbers for budget.
* **Sorting (Bonus Feature):** View destinations sorted by start date or budget.

---

## 🏗️ Technical Architecture (OOP Design)

The project adheres to Object-Oriented Programming principles, organized into three main classes:

1.  **`Destination` Class:**
    * **Attributes:** `city`, `country`, `start_date`, `end_date`, `budget`, `activities`.
    * **Methods:** `update_details()`, `__str__()` (for display), `to_dict()`, `from_dict()` (for JSON serialization/deserialization).

2.  **`ItineraryManager` Class:**
    * Manages the collection of `Destination` objects.
    * **Attributes:** `destinations` (a list of `Destination` objects).
    * **Methods:** `add_destination()`, `remove_destination()`, `update_destination()`, `search_destination()`, `view_all_destinations()`, `save_to_file()`, `load_from_file()`, `ai_assistance_menu()`.

3.  **`AITravelAssistant` Class:**
    * Handles all interactions with the external AI API.
    * **Methods:** `generate_itinerary(destination)`, `generate_budget_tips(destination)`, and an internal `_make_api_call()` method with robust error handling and exponential backoff.

---

## ⚙️ Technologies Used

* **Python 3.x:** The core programming language.
* **`requests`:** For making HTTP requests to the OpenAI/Gemini API.
* **`json`:** For reading from and writing to JSON files (data persistence).
* **`datetime`:** For date validation and manipulation.
* **`tabulate`:** For pretty-printing tabular data in the console.
* **OpenAI API (or Google Gemini API):** For AI-powered itinerary generation and tips.

---

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HasiniAnuththara/AI-Travel-Itinerary-Planner.git](https://github.com/HasiniAnuththara/AI-Travel-Itinerary-Planner.git)
    cd AI-Travel-Itinerary-Planner
    ```

2.  **Install dependencies:**
    ```bash
    pip install requests tabulate
    ```

3.  **Set up your API Key:**
    * Obtain an API key from [OpenAI](https://platform.openai.com/) or [Google AI Studio](https://makersuite.google.com/) (for Gemini).
    * Open the `travel_planner.py` file.
    * Find the line `OPENAI_API_KEY = ""` and replace the empty string with your actual API key.
        ```python
        OPENAI_API_KEY = "your_actual_api_key_here"
        ```
    * If you're using a Google Gemini model, you might also need to adjust `self.api_url` and `self.model_name` within the `AITravelAssistant` class as commented in the code.

4.  **Run the application:**
    ```bash
    python travel_planner.py
    ```

---

## 📂 File Structure

# ✈️ AI Travel Itinerary Planner

## Project Overview

The **AI Travel Itinerary Planner** is a command-line application built with Python that serves as a smart travel companion. It allows users to **manage their travel destinations** (add, remove, update, view, search) and leverages **Artificial Intelligence (AI)** through OpenAI (or Google Gemini) Chat Completions to generate personalized daily travel itineraries and budget-saving tips. This project demonstrates strong skills in Object-Oriented Programming (OOP), data persistence (JSON file handling), and API integration.

---

## ✨ Features

* **Add Destinations:** Create `Destination` objects with details like city, country, travel dates, budget, and a list of activities.
* **Remove Destinations:** Easily remove destinations by specifying the city name.
* **Update Destinations:** Modify any detail of an existing destination.
* **View All Destinations:** Display all saved destinations in a clear, tabular format.
* **Search Destinations:** Find specific trips by city, country, or keywords in activities.
* **Save Itinerary:** Persist all destination data to a `destinations.json` file.
* **Load Itinerary:** Automatically load saved destinations upon application startup.
* **AI Travel Assistance:**
    * **Generate Daily Itinerary:** Get a detailed day-by-day travel plan for a selected destination, customized by dates, budget, and activities.
    * **Generate Budget Tips:** Receive practical advice on saving money for your trip.
* **Data Validation:** Ensures correct input formats for dates and positive numbers for budget.
* **Sorting (Bonus Feature):** View destinations sorted by start date or budget.

---

## 🏗️ Technical Architecture (OOP Design)

The project adheres to Object-Oriented Programming principles, organized into three main classes:

1.  **`Destination` Class:**
    * **Attributes:** `city`, `country`, `start_date`, `end_date`, `budget`, `activities`.
    * **Methods:** `update_details()`, `__str__()` (for display), `to_dict()`, `from_dict()` (for JSON serialization/deserialization).

2.  **`ItineraryManager` Class:**
    * Manages the collection of `Destination` objects.
    * **Attributes:** `destinations` (a list of `Destination` objects).
    * **Methods:** `add_destination()`, `remove_destination()`, `update_destination()`, `search_destination()`, `view_all_destinations()`, `save_to_file()`, `load_from_file()`, `ai_assistance_menu()`.

3.  **`AITravelAssistant` Class:**
    * Handles all interactions with the external AI API.
    * **Methods:** `generate_itinerary(destination)`, `generate_budget_tips(destination)`, and an internal `_make_api_call()` method with robust error handling and exponential backoff.

---

## ⚙️ Technologies Used

* **Python 3.x:** The core programming language.
* **`requests`:** For making HTTP requests to the OpenAI/Gemini API.
* **`json`:** For reading from and writing to JSON files (data persistence).
* **`datetime`:** For date validation and manipulation.
* **`tabulate`:** For pretty-printing tabular data in the console.
* **OpenAI API (or Google Gemini API):** For AI-powered itinerary generation and tips.

---

## 🚀 How to Run

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/HasiniAnuththara/AI-Travel-Itinerary-Planner.git](https://github.com/HasiniAnuththara/AI-Travel-Itinerary-Planner.git)
    cd AI-Travel-Itinerary-Planner
    ```

2.  **Install dependencies:**
    ```bash
    pip install requests tabulate
    ```

3.  **Set up your API Key:**
    * Obtain an API key from [OpenAI](https://platform.openai.com/) or [Google AI Studio](https://makersuite.google.com/) (for Gemini).
    * Open the `travel_planner.py` file.
    * Find the line `OPENAI_API_KEY = ""` and replace the empty string with your actual API key.
        ```python
        OPENAI_API_KEY = "your_actual_api_key_here"
        ```
    * If you're using a Google Gemini model, you might also need to adjust `self.api_url` and `self.model_name` within the `AITravelAssistant` class as commented in the code.

4.  **Run the application:**
    ```bash
    python travel_planner.py
    ```

---

## 📂 File Structure

## 💡 Future Enhancements

* **User Authentication:** Implement user accounts for personalized itineraries.
* **Web Interface:** Develop a graphical user interface (GUI) using Flask/Django or a front-end framework like React.
* **Advanced AI Prompts:** Allow users to specify preferences for itinerary style (e.g., adventurous, relaxing, family-friendly).
* **Currency Conversion:** Integrate a currency API to handle budgets in different currencies.
* **Integration with Maps/Weather:** Add links or display real-time weather/map data for destinations.
