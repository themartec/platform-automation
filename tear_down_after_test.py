import os
import platform
import configparser
import sys

os_platform = platform.platform()
python_version = sys.version
browser_type = sys.argv[2]
browser_version = ''
env_input = sys.argv[1]

if env_input == '1':
    env_info = "staging"
elif env_input == '2':
    env_info = "dev"
elif env_input == '0':
    env_info = "production"
else:
    env_info = "undefined"

print(f"    - os_platform: {os_platform}")
print(f"    - python_version: {python_version}")
print(f"    - browser_type: {browser_type}")
print(f"    - browser_version: {browser_version}")
print(f"    - env_info: {env_info}")

config = configparser.ConfigParser()
config['DEFAULT'] = {'os_platform': os_platform,
                     'python_version': python_version,
                     'env_info': env_info,
                     'browser_type': browser_type}

if os.path.exists('allure-results'):
    with open('allure-results/environment.properties', 'w') as configfile:
        config.write(configfile)
