import os
import time
import json
import logging

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

from bots.instahyre_bot import InstahyreBot
from bots.hirist_bot import HiristBot

SUPPORTED_PLATFORMS = ["instahyre", "hirist"]

class JobApplyManager:
    """
    Manages user credentials and job application process for supported platforms.
    """

    def __init__(self):
        self.user_key = None
        self.platform = ""
        self.skills = []
        self.yoe = 0
        self.locations = []
        self.search_mode = False
        self.credentials = self.load_credentials()

    def load_credentials(self):
        """
        Loads credentials from config/credentials.json.
        Returns an empty dict if file is missing or invalid.
        """
        cred_path = os.path.join("config", "credentials.json")
        if not os.path.exists(cred_path):
            sample_path = os.path.join("config", "credentials.sample.json")
            if os.path.exists(sample_path):
                logging.info("Please copy 'credentials.sample.json' to 'credentials.json' and fill in your details.")
            else:
                logging.warning("No credentials file found. Please create one in the config folder.")
            return {}
        try:
            with open(cred_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logging.error(f"Error loading credentials: {e}")
            return {}

    def get_user_profile(self):
        """
        Prompts for user profile and ensures credentials exist for the user.
        """
        if not self.credentials:
            logging.warning("No credentials loaded. You will be prompted to enter credentials.")
        else:
            logging.info(f"Available users: {', '.join(self.credentials.keys())}")
            time.sleep(0.1)
        self.user_key = input("Enter your user (or new user): ").strip()
        if self.user_key not in self.credentials:
            self.credentials[self.user_key] = {}
        return self.user_key

    def get_user_input(self):
        """
        Prompts user for platform and search mode, with input validation.
        """
        while True:
            self.platform = input(f"Choose platform ({'/'.join(SUPPORTED_PLATFORMS)}): ").strip().lower()
            if self.platform in SUPPORTED_PLATFORMS:
                break
            logging.info(f"Invalid platform. Please choose from {', '.join(SUPPORTED_PLATFORMS)}.")

        while True:
            mode = input("Apply only recommended jobs? (yes/no): ").strip().lower()
            if mode in ["yes", "no"]:
                break
            logging.info("Please enter 'yes' or 'no'.")
        self.search_mode = mode != "yes"
        if self.search_mode:
            self.skills = input("Enter skills (comma separated): ").strip().split(",")
            self.yoe = input("Enter years of experience: ").strip()
            self.locations = input("Enter preferred locations (comma separated), Type 'ALL' if no preference: ").strip().split(",")

    def get_creds(self, platform):
        """
        Gets credentials for the given platform, prompting the user if missing.
        """
        user_creds = self.credentials.get(self.user_key, {})
        cred_path = os.path.join("config", "credentials.json")
        if platform in user_creds:
            return user_creds[platform]["email"], user_creds[platform]["password"]
        else:
            logging.warning("WARNING: Your credentials will be stored in plain text in 'config/credentials.json'.")
            email = input(f"Enter email for {platform}: ")
            password = input(f"Enter password for {platform}: ")
            self.credentials[self.user_key][platform] = {"email": email, "password": password}
            try:
                with open(cred_path, "w") as f:
                    json.dump(self.credentials, f, indent=4)
            except Exception as e:
                logging.error(f"Failed to save credentials: {e}")
            return email, password

    def run(self):
        """
        Main entry point for the job application process.
        """
        self.get_user_profile()
        self.get_user_input()
        email, password = self.get_creds(self.platform)

        if self.platform == "instahyre":
            job_functions_roles = ''
            job_funcs = input("Do you want to apply based on job functions (yes/no): ")
            if job_funcs == "yes":
                job_functions_roles = input("Enter the job function you want to apply (eg:- 'SDET', "
                                            "'All - Software Engineering'): ")
            logging.info("Starting Instahyre bot...")
            bot = InstahyreBot(email, password, self.skills, self.yoe, self.locations, self.search_mode, job_functions_roles)
        elif self.platform == "hirist":
            logging.info("Starting Hirist bot...")
            bot = HiristBot(email, password, self.skills, self.yoe, self.locations, self.search_mode)
            # bot.apply_jobs()
        else:
            logging.error(f"Unsupported platform: {self.platform}")
            return
        
        bot.run()

if __name__ == "__main__":
    manager = JobApplyManager()
    manager.run()