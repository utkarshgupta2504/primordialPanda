import os


_files = [
    "channelsToBeDeleted.json",
    "customChannels.json",
    "customReacts.json",
    "experience.json",
    "highlights.json",
    "reminders.json",
    "weeklyLeaderboard.json",
    "config.json",
]


def checkFiles():
    for file in _files:
        if not os.path.exists(f"database/{file}"):
            with open(f"database/{file}", "w") as f:
                if file not in {"weeklyOwOCount.json", "dailyOwOCount.json"}:
                    f.write("{}")
                else:
                    f.write(
                        '{\n\t"lastTime": 0,\n\t"previous": {},\n\t"current": {}\n}'
                    )
