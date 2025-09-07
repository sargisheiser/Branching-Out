import json
import re
from pathlib import Path
from typing import List, Dict, Any

DATA_FILE = Path("users.json")

def load_users() -> List[Dict[str, Any]]:
   """
   Load user data from users.json.
   Returns: A list of user dictionaries.
   Raises:
       FileNotFoundError: If the file does not exist.
       ValueError: If the JSON is invalid or empty.
   """
   try:
       with DATA_FILE.open("r", encoding="utf-8") as file:
           users = json.load(file)
       if not isinstance(users, list):
           raise ValueError("users.json must contain a list of users")
       return users
   except FileNotFoundError:
       print("users.json not found.")
       raise
   except json.JSONDecodeError as exc:
       print(f"Invalid JSON format in {DATA_FILE}: {exc}")
       raise

def filter_users_by_name(users: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
   """Return users matching the given name (case-insensitive)."""
   return [user for user in users if user.get("name", "").lower() == name.lower()]

def filter_by_age(users: List[Dict[str, Any]], age: str) -> List[Dict[str, Any]]:
   """Return users with the given age, validating numeric input."""
   if not age.isdigit():
       print("Invalid age: must be a number.")
       return []
   return [user for user in users if str(user.get("age")) == age]

def filter_by_email(users: List[Dict[str, Any]], email: str) -> List[Dict[str, Any]]:
   """Return users matching the given email (case-insensitive), with format check."""
   if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
       print("Invalid email format.")
       return []
   return [user for user in users if user.get("email", "").lower() == email.lower()]

def display_results(results: List[Dict[str, Any]]) -> None:
   """Pretty-print the list of filtered users."""
   if not results:
       print("No matching users found.")
       return
   for user in results:
       print(user)

def main() -> None:
   try:
       users = load_users()
   except (FileNotFoundError, ValueError):
       return

   option = input("Filter by 'name', 'age', or 'email': ").strip().lower()

   if option == "name":
       name = input("Enter a name to filter users: ").strip()
       results = filter_users_by_name(users, name)
   elif option == "age":
       age = input("Enter an age to filter users: ").strip()
       results = filter_by_age(users, age)
   elif option == "email":
       email = input("Enter an email to filter users: ").strip()
       results = filter_by_email(users, email)
   else:
       print("Unsupported filter option.")
       return

   display_results(results)

if __name__ == "__main__":
   main()
