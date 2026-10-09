import os


try:
    home_dir = os.environ["HOME"]
    print(f"Home directory is: {home_dir}")

    # print(dict(os.environ))
    print(os.getenv("LOGNAME"))
    api_key = os.environ["API_KEY"]
    print(f"API Key is: {api_key}")

    

except KeyError as e:
    print(f"Error: Environment variable {e} not found!")


