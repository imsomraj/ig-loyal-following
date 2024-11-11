import instaloader
import getpass
from colorama import Fore, init
import time
import os

def fetch_users(profile, fetch_function, batch_size=100):
    users = set()
    count = 0
    for user in fetch_function():
        users.add(user.username)
        count += 1
        if count % batch_size == 0:
            time.sleep(2)  # Adjust delay between batches
    return users

def check_followers(logged_in_username, password, target_username):
    try:
        # Initialize colorama
        init(autoreset=True)

        # Create an instance of Instaloader
        L = instaloader.Instaloader()

        # Load session if it exists
        session_file = f'/content/drive/MyDrive/{logged_in_username}_session'  # Google Drive path
        if os.path.exists(session_file):
            L.load_session_from_file(logged_in_username, filename=session_file)
        else:
            # Log in to Instagram with the primary account
            L.login(logged_in_username, password)
            L.save_session_to_file(filename=session_file)

        # Load the target profile
        profile = instaloader.Profile.from_username(L.context, target_username)

        # Get the list of followings and followers
        print("Fetching followings...")
        followings = fetch_users(profile, profile.get_followees)

        print("Fetching followers...")
        followers = fetch_users(profile, profile.get_followers)

        # Check if followings are in followers
        following_back = [user for user in followings if user in followers]
        not_following_back = [user for user in followings if user not in followers]

        # Output the result
        print(Fore.GREEN + "These accounts are following you back:")
        for user in following_back:
            print(user)

        print(Fore.RED + "\nThese accounts are not following you back:")
        for user in not_following_back:
            print(user)
    
    except instaloader.exceptions.ProfileNotExistsException:
        print(f"The profile '{target_username}' does not exist.")
    except instaloader.exceptions.LoginRequiredException:
        print("Login failed. Please check your username and password.")
    except instaloader.exceptions.TwoFactorAuthRequiredException:
        print("Two-factor authentication is required. Please enable and configure 2FA.")
    except instaloader.exceptions.QueryReturnedBadRequestException:
        print("Instagram returned a bad request error. Try again later.")
    except instaloader.exceptions.ConnectionException:
        print("Connection error occurred. Try again later.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Main program
logged_in_username = input("Enter your Instagram username: ")
password = getpass.getpass("Enter your Instagram password: ")
target_username = input("Enter the target Instagram username: ")
check_followers(logged_in_username, password, target_username)
