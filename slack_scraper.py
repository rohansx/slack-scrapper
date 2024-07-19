# slack_scraper.py

import requests
import time
import json
from config import SLACK_URL, COOKIES, CHANNEL_ID, HEADERS

def get_members(channel_id):
    members = []
    cursor = ""
    while True:
        response = requests.get(
            f"{SLACK_URL}/api/conversations.members",
            headers=HEADERS,
            cookies=COOKIES,
            params={
                "channel": channel_id,
                "limit": 1000,
                "cursor": cursor
            }
        )
        data = response.json()

        # Print the entire response for debugging
        print(json.dumps(data, indent=2))

        if 'error' in data:
            raise Exception(f"Error fetching members: {data['error']}")

        if 'members' not in data:
            raise Exception(f"'members' key not found in response. Response: {data}")

        members.extend(data['members'])
        cursor = data.get('response_metadata', {}).get('next_cursor', "")
        if not cursor:
            break
        time.sleep(1)  # Add a delay to handle rate limiting
    return members

if __name__ == "__main__":
    members = get_members(CHANNEL_ID)
    with open('members.json', 'w') as f:
        json.dump(members, f)
    print(f"Saved {len(members)} members to members.json.")
