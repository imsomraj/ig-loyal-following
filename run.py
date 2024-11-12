import instaloader
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
            time.sleep(15)  # Adjust delay between batches
    return users

def check_followers(logged_in_username, password, target_username):
    try:
        print("Initializing InstaLoader...")  # Debugging line
        # Initialize colorama
        init(autoreset=True)

        # Create an instance of Instaloader
        L = instaloader.Instaloader()

        # Log in to Instagram with the primary account
        print("Logging in...")  # Debugging line
        L.login(logged_in_username, password)

        # Load the target profile
        print(f"Fetching profile for {target_username}...")  # Debugging line
        profile = instaloader.Profile.from_username(L.context, target_username)

        # Get the list of followings and followers
        print("Fetching followings...")  # Debugging line
        followings = fetch_users(profile, profile.get_followees, batch_size=20)

        print("Fetching followers...")  # Debugging line
        followers = fetch_users(profile, profile.get_followers, batch_size=20)

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

# Hardcoded credentials
logged_in_username = "bakchodii.central"
password = "divyahaha"
target_username = "somrajpaul_"

# Run the function
check_followers(logged_in_username, password, target_username)
