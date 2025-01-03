from datetime import datetime
import json
import time
from colorama import Fore
import requests
import random


class terminal:
    BASE_URL = "https://app.0xterminal.game/api/"
    HEADERS = {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "en-GB,en;q=0.9,en-US;q=0.8",
        "content-type": "application/json",
        "priority": "u=1, i",
        "referer": "https://app.0xterminal.game/app",
        "sec-ch-ua": '"Microsoft Edge";v="131", "Chromium";v="131", "Not_A Brand";v="24", "Microsoft Edge WebView2";v="131"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "if-none-match": 'W/"21a-y+T53dCeOf899eNKEl1z3T7wCec":',
    }

    def __init__(self):
        self.query_list = self.load_query("query.txt")
        self.token = None
        self.coins = 0

    def banner(self) -> None:
        """Displays the banner for the bot."""
        self.log("🎉 Terminal Station Free Bot", Fore.CYAN)
        self.log("🚀 Created by LIVEXORDS", Fore.CYAN)
        self.log("📢 Channel: t.me/livexordsscript\n", Fore.CYAN)

    def log(self, message, color=Fore.RESET):
        print(
            Fore.LIGHTBLACK_EX
            + datetime.now().strftime("[%Y:%m:%d ~ %H:%M:%S] |")
            + " "
            + color
            + message
            + Fore.RESET
        )

    def load_config(self) -> dict:
        """Loads configuration from config.json."""
        try:
            with open("config.json", "r") as config_file:
                return json.load(config_file)
        except FileNotFoundError:
            self.log("❌ File config.json not found!", Fore.RED)
            return {}
        except json.JSONDecodeError:
            self.log("❌ Error reading config.json!", Fore.RED)
            return {}

    def load_query(self, path_file="query.txt") -> list:
        self.banner()

        try:
            with open(path_file, "r") as file:
                queries = [line.strip() for line in file if line.strip()]

            if not queries:
                self.log(f"⚠️ Warning: {path_file} is empty.", Fore.YELLOW)

            self.log(f"✅ Loaded: {len(queries)} queries.", Fore.GREEN)
            return queries

        except FileNotFoundError:
            self.log(f"❌ File not found: {path_file}", Fore.RED)
            return []
        except Exception as e:
            self.log(f"❌ Error loading queries: {e}", Fore.RED)
            return []

    def login(self, index: int) -> None:
        self.log("\U0001F512 Attempting to log in...", Fore.GREEN)

        if index >= len(self.query_list):
            self.log("\u274C Invalid login index. Please check again.", Fore.RED)
            return

        req_url = f"{self.BASE_URL}statistic/user"
        token = self.query_list[index]

        self.log(
            f"\U0001F4CB Using token: {token[:10]}... (truncated for security)",
            Fore.CYAN,
        )

        headers = {**self.HEADERS, "cookie": token}

        try:
            self.log(
                "\U0001F4E1 Sending request to fetch user statistics...",
                Fore.CYAN,
            )

            response = requests.get(req_url, headers=headers)
            if response.status_code == 304:
                self.log("\u26A0 Received status 304: Not Modified.", Fore.YELLOW)
                self.log(f"Response: {response.text}", Fore.YELLOW)
                return

            response.raise_for_status()
            data = response.json()

            info = data.get("info", {})
            stats = data.get("statistic", {})
            pack_stats = data.get("packStatistic", {})
            referral_stats = data.get("referralStatistic", {})

            username = info.get("telegram", {}).get("username", "Unknown")
            telegram_id = info.get("telegram", {}).get("id", "Unknown")
            ton_balance = stats.get("tonBalance", "0")
            terminal_balance = stats.get("terminalBalance", 0)
            next_harvest = stats.get("nextHarvestTimestamp", "Unknown")
            total_quests = stats.get("totalCompletedQuests", 0)

            self.token = token

            self.log("\u2705 Login successful!", Fore.GREEN)
            self.log(f"\U0001F464 Telegram Username: {username}", Fore.LIGHTGREEN_EX)
            self.log(f"\U0001F4F2 Telegram ID: {telegram_id}", Fore.CYAN)
            self.log(f"\U0001FA99 TON Balance: {ton_balance}", Fore.LIGHTBLUE_EX)
            self.log(
                f"\U0001FA9A Terminal Balance: {terminal_balance}", Fore.LIGHTMAGENTA_EX
            )
            self.log(
                f"\U0001F4C5 Next Harvest Timestamp: {next_harvest}", Fore.LIGHTCYAN_EX
            )
            self.log(
                f"\U0001F4DA Total Completed Quests: {total_quests}",
                Fore.LIGHTYELLOW_EX,
            )

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Failed to send login request: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Data error (possible JSON issue): {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Key error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Unexpected error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )

    def harvest(self) -> None:
        """Harvest rewards from the server."""
        req_url_harvest = f"{self.BASE_URL}game/harvest"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001F331 Harvesting rewards...", Fore.CYAN)
            response = requests.post(req_url_harvest, headers=headers)

            # Check for successful status code (201)
            if response.status_code == 201:
                self.log("\u2705 Harvest successful!", Fore.GREEN)
            else:
                self.log(
                    f"\u274C Harvest failed with status code: {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Response: {response.text}", Fore.YELLOW)
                return

            # Parse the JSON response
            data = response.json()
            claimed_terminal = data.get("claimedTerminal", 0)
            claimed_ton = data.get("claimedTon", "0")
            next_harvest_timestamp = data.get("nextHarvestTimestamp", 0)
            terminal_total = data.get("terminalTotal", 0)
            ton_total = data.get("tonTotal", "0")

            # Convert timestamp to hours, minutes, seconds
            remaining_time = next_harvest_timestamp // 1000 - int(time.time())
            hours, remainder = divmod(remaining_time, 3600)
            minutes, seconds = divmod(remainder, 60)

            # Log details
            self.log(
                f"\U0001FA9A Claimed Terminal: {claimed_terminal}", Fore.LIGHTBLUE_EX
            )
            self.log(f"\U0001FA99 Claimed TON: {claimed_ton}", Fore.LIGHTCYAN_EX)
            self.log(
                f"\U0001FA9A Total Terminal: {terminal_total}", Fore.LIGHTMAGENTA_EX
            )
            self.log(f"\U0001FA99 Total TON: {ton_total}", Fore.LIGHTGREEN_EX)
            self.log(
                f"\U0001F552 Next harvest available in: {hours}h {minutes}m {seconds}s",
                Fore.LIGHTYELLOW_EX,
            )

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Failed to send harvest request: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Data error (possible JSON issue): {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Key error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Unexpected error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )

    def quest(self) -> None:
        """Fetch and review quests from the server."""
        # Fetch all quests
        req_url_quests = f"{self.BASE_URL}quest/all"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001F4D6 Fetching available quests...", Fore.CYAN)
            response = requests.get(req_url_quests, headers=headers)

            if response.status_code != 200:
                self.log(
                    f"\u274C Failed to fetch quests: Status code {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Response: {response.text}", Fore.YELLOW)
                return

            # Parse the response for quest data
            data = response.json()
            quests = data.get("quests", [])

            if not quests:
                self.log("\U0001F614 No quests available to process.", Fore.YELLOW)
                return

            self.log(f"\U0001F4DA Found {len(quests)} quests to review.", Fore.GREEN)

            for quest in quests:
                quest_id = quest.get("id")
                quest_name = quest.get("name", "Unknown Quest")
                quest_status = quest.get("status", "Unknown")
                quest_reward = quest.get("reward", 0)
                quest_link = quest.get("actionLink", "No Link")

                self.log(
                    f"\U0001F539 Quest: {quest_name} (ID: {quest_id})",
                    Fore.LIGHTCYAN_EX,
                )
                self.log(
                    f"  \U0001F4B8 Reward: {quest_reward} | Status: {quest_status}",
                    Fore.LIGHTMAGENTA_EX,
                )
                self.log(f"  \U0001F517 Action Link: {quest_link}", Fore.LIGHTBLUE_EX)

                if quest_status != "OPENED":
                    self.log(
                        f"  \U0001F6AB Skipping quest {quest_id} - Not opened.",
                        Fore.YELLOW,
                    )
                    continue

                # Submit quest for review
                req_url_review = f"{self.BASE_URL}quest/review"
                payload = {"questId": quest_id}
                self.log(
                    f"\U0001F4E1 Submitting quest {quest_id} for review...", Fore.CYAN
                )

                review_response = requests.post(
                    req_url_review, headers=headers, json=payload
                )

                if review_response.status_code == 201:
                    self.log(
                        f"\U0001F4AA Quest {quest_id} reviewed successfully!",
                        Fore.GREEN,
                    )
                else:
                    self.log(
                        f"\u274C Failed to review quest {quest_id}: Status code {review_response.status_code}",
                        Fore.RED,
                    )
                    self.log(f"Response: {review_response.text}", Fore.YELLOW)
                    continue

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Failed to process quests: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except ValueError as e:
            self.log(f"\u274C Data error (possible JSON issue): {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except KeyError as e:
            self.log(f"\u274C Key error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )
        except Exception as e:
            self.log(f"\u274C Unexpected error: {e}", Fore.RED)
            self.log(
                f"Response: {getattr(response, 'text', 'No response text available')}",
                Fore.YELLOW,
            )

    def game_coin_flip(self) -> None:
        """Play the Coin Flip game, analyze flip history to predict outcomes, or randomly guess if no history is available."""
        # Fetch coin flip stats
        stats_url = f"{self.BASE_URL}game/coinflip/stats"
        headers = {**self.HEADERS, "cookie": self.token}

        try:
            self.log("\U0001FA99 Fetching Coin Flip stats...", Fore.CYAN)
            response = requests.get(stats_url, headers=headers)

            if response.status_code != 200:
                self.log(
                    f"\u274C Failed to fetch stats: Status code {response.status_code}",
                    Fore.RED,
                )
                self.log(f"Response: {response.text}", Fore.YELLOW)
                return

            stats = response.json()
            terminal_games_left = stats.get("terminalGamesLeft", 0)
            flip_history = stats.get("flipHistory", [])
            min_bet = stats.get("minBetTerminal", "50")
            max_bet = stats.get("maxBetTerminal", "5000")

            self.log(f"\U0001F4AA Games Left: {terminal_games_left}", Fore.GREEN)
            self.log(f"\U0001F4B0 Bet Range: {min_bet} - {max_bet}", Fore.LIGHTCYAN_EX)

            if not flip_history:
                self.log(
                    "\U0001F614 No flip history available, guessing randomly.",
                    Fore.YELLOW,
                )

            # Analyze flip patterns
            pattern = {}
            for flip in flip_history:
                session_id = flip.get("sessionId")
                side = flip.get("side")
                if session_id not in pattern:
                    pattern[session_id] = []
                pattern[session_id].append(side)

            self.log("\U0001F52E Analyzing flip patterns...", Fore.BLUE)
            for session, flips in pattern.items():
                self.log(
                    f"  Session {session}: {', '.join(flips)}", Fore.LIGHTMAGENTA_EX
                )

            # Function to predict guess
            def predict_guess(flip_history: list) -> str:
                if not flip_history:
                    return random.choice(["HEADS", "TAILS"])
                tails_count = sum(
                    1 for flip in flip_history if flip.get("side") == "TAILS"
                )
                heads_count = sum(
                    1 for flip in flip_history if flip.get("side") == "HEADS"
                )
                if tails_count > heads_count:
                    return "HEADS"
                elif heads_count > tails_count:
                    return "TAILS"
                else:
                    return random.choice(["HEADS", "TAILS"])

            # Play the game
            bet_url = f"{self.BASE_URL}game/coinflip/bet"
            flip_url = f"{self.BASE_URL}game/coinflip/flip"
            while terminal_games_left > 0:
                guess = predict_guess(flip_history)
                payload = {"token": "TERMINAL", "bet": min_bet, "guess": guess}

                self.log(f"\U0001F3B2 Guessing: {guess}...", Fore.CYAN)
                bet_response = requests.post(bet_url, headers=headers, json=payload)

                if bet_response.status_code == 400:
                    error_message = bet_response.json().get("message", "")
                    if "active coinflip session" in error_message:
                        self.log(
                            "\U0001F6A7 Active session detected. Resolving it...",
                            Fore.YELLOW,
                        )
                        resolve_payload = {"guess": "HEADS"}
                        flip_response = requests.post(
                            flip_url, headers=headers, json=resolve_payload
                        )

                        if flip_response.status_code == 201:
                            self.log(
                                "\U0001F389 Active session resolved successfully.",
                                Fore.GREEN,
                            )
                            continue
                        else:
                            self.log(
                                f"\u274C Failed to resolve session: {flip_response.status_code}",
                                Fore.RED,
                            )
                            self.log(f"Response: {flip_response.text}", Fore.YELLOW)
                            return

                elif bet_response.status_code != 201:
                    self.log(
                        f"\u274C Failed to play: Status code {bet_response.status_code}",
                        Fore.RED,
                    )
                    self.log(f"Response: {bet_response.text}", Fore.YELLOW)
                    break

                game_result = bet_response.json()
                session = game_result.get("session", {})
                status = session.get("status", "UNKNOWN")
                flips = session.get("flips", [])
                reward = session.get("reward", "0")
                next_reward = session.get("nextReward", "0")

                self.log(
                    f"\U0001F4A1 Result: {status}",
                    Fore.GREEN if status == "WIN" else Fore.RED,
                )
                self.log(f"  Flips: {', '.join(flips)}", Fore.LIGHTBLUE_EX)
                self.log(
                    f"  Reward: {reward} | Next Reward: {next_reward}",
                    Fore.LIGHTCYAN_EX,
                )

                if status == "WIN":
                    self.log("\U0001F389 You won this round!", Fore.GREEN)
                else:
                    self.log("\U0001F614 Better luck next time.", Fore.YELLOW)

                for flip in flips:
                    flip_history.append(
                        {"side": flip, "sessionId": terminal_games_left}
                    )

                terminal_games_left -= 1
                self.log(f"\U0001F4AA Games Left: {terminal_games_left}", Fore.GREEN)

        except requests.exceptions.RequestException as e:
            self.log(f"\u274C Failed to fetch or play the game: {e}", Fore.RED)
        except Exception as e:
            self.log(f"\u274C Unexpected error: {e}", Fore.RED)


if __name__ == "__main__":
    ter = terminal()
    index = 0
    max_index = len(ter.query_list)
    config = ter.load_config()

    if max_index == 0:
        ter.log(
            "❌ [ERROR] Query list is empty. Please check your configuration.", Fore.RED
        )
        exit()

    ter.log(
        "🎉 [LIVEXORDS] === Welcome to Terminal Station Automation === [LIVEXORDS]",
        Fore.YELLOW,
    )
    ter.log(f"📂 Loaded {max_index} accounts from query list.", Fore.YELLOW)

    while True:
        current_account = ter.query_list[index]
        display_account = (
            current_account[:10] + "..."
            if len(current_account) > 10
            else current_account
        )

        ter.log(
            f"👤 [ACCOUNT] Processing account {index + 1}/{max_index}: {display_account}",
            Fore.YELLOW,
        )

        try:
            ter.login(index)
        except Exception as e:
            ter.log(
                f"❌ [ERROR] Failed to log in with account {index + 1}: {e}", Fore.RED
            )
            continue

        ter.log("🛠️ Starting task execution...")
        tasks = {
            "harvest": "🌾 Collect Daily Rewards",
            "quest": "🃏 Complete Card Quests",
            "game_coin_flip": "🎲 Play Coin Flip Game",
        }

        for task_key, task_name in tasks.items():
            task_status = config.get(task_key, False)
            ter.log(
                f"[CONFIG] {task_name}: {'✅ Enabled' if task_status else '❌ Disabled'}",
                Fore.YELLOW if task_status else Fore.RED,
            )

            if task_status:
                if hasattr(ter, task_key):
                    try:
                        ter.log(f"🔄 Executing {task_name}...")
                        getattr(ter, task_key)()
                    except Exception as e:
                        ter.log(
                            f"❌ [ERROR] Failed to execute {task_name}: {e}", Fore.RED
                        )
                else:
                    ter.log(
                        f"❌ [ERROR] Task {task_name} not found in terminal instance.",
                        Fore.RED,
                    )

        if index == max_index - 1:
            ter.log("🔁 All accounts processed. Restarting loop.")
            ter.log(
                f"⏳ Sleeping for {config.get('delay_loop', 30)} seconds before restarting."
            )
            time.sleep(config.get("delay_loop", 30))
            index = 0
        else:
            ter.log(
                f"➡️ Switching to the next account in {config.get('delay_account_switch', 10)} seconds."
            )
            time.sleep(config.get("delay_account_switch", 10))
            index += 1
