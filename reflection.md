# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

When I first ran the game, it looked functional at a glance, but once I started interacting with it, several logic issues became obvious. The UI worked, and I could enter guesses, but the game behavior did not match what I expected from a normal number guessing game. It felt like the logic behind the scenes was inconsistent even though the interface looked clean.

Two clear bugs I noticed were that the hint messages were backwards and the attempts counter was incorrect. For example, when I guessed a number higher than the secret, the app told me to go higher instead of lower. I also saw that attempts started at 1 instead of 0, which made the attempts left display inaccurate from the beginning. Another issue was that starting a new game did not fully reset the state, so previous values like score and history could carry over.

---

## 2. How did you use AI as a teammate?

I used ChatGPT as my main AI teammate throughout this assignment. I shared my code and asked it to help identify bugs, explain what was wrong, and suggest fixes while keeping my original structure. I mainly used it to reason through logic issues rather than just copy solutions.

One AI suggestion that was correct was identifying that the hint logic in `check_guess()` was reversed. It explained that if the guess is greater than the secret, the message should say to go lower, not higher. I verified this by reading the condition carefully and testing it in the running app.

One AI suggestion that was misleading was an earlier version that rewrote too much of the code. While it fixed the bugs, it changed more structure and naming than necessary for this assignment. I verified that by comparing it with my original file and decided to keep the same functions and variables while only fixing the actual bugs.

---

## 3. Debugging and testing your fixes

I decided a bug was fixed only after checking both the logic and the actual behavior in the app. First, I made sure the code made sense logically, and then I ran the Streamlit app to confirm that the user experience matched expectations. This helped me avoid trusting changes just because they looked correct in code.

One test I ran using pytest was checking that `check_guess(60, 50)` returns `("Too High", "📉 Go LOWER!")`. This confirmed that the hint logic was fixed correctly. I also manually tested invalid inputs like empty strings and decimals to make sure they were rejected properly without affecting attempts.

AI helped me think about testing more clearly by suggesting that I test the helper functions separately. That made debugging easier because I could isolate problems in parsing, comparison, and scoring without relying only on the full app.

---

## 4. What did you learn about Streamlit and state?

I would explain Streamlit reruns like this: every time the user interacts with the app, the entire script runs again from the top. Because of that, if values are not stored in `st.session_state`, they can reset or behave unexpectedly. Session state is what allows the app to remember important values like the secret number, attempts, score, and history.

This project helped me understand that many of the bugs were actually state-related. Things like difficulty changes and starting a new game required careful resetting of session variables. It showed me that even simple apps need proper state management to behave correctly.

---

## 5. Looking ahead: your developer habits

One habit I want to keep using is marking bugs clearly before fixing them. Adding `# FIXME:` comments helped me focus on one issue at a time and made the debugging process more structured. It also made it easier to connect each fix to a specific problem.

One thing I would do differently next time is be more precise when asking AI for help. Instead of asking for general fixes, I would ask for smaller, targeted changes so I can better understand and verify each one.

This project changed how I think about AI-generated code because it showed me that code can look clean and still contain logical errors. AI was helpful for spotting patterns and suggesting fixes, but I still had to verify everything myself. It reinforced that testing and careful reasoning are more important than just trusting the code output.