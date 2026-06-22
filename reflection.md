# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
The game opens as a streamlit app with a "Settings" panel in the left (showing options for difficulty and information on the number of allowed attempts). The Game window is to the right of the side panel. It has prompts to make a guess, a dropdown tab for Developer Debug Info, a box to enter a guess and buttons to submit a guess, reload to a new game and to show a hint. There is also a cheeky little disclaimer at the bottom of the screen stating that this ai-generated game claimed the code was "production-ready" 😂.

- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").
The first time I ran it, I noticed 3 errors. First, the feedback says to go higher when you have guessed a number larger than the target, while prompting you to go lower if you are below the target

The game wouldn't restart unless I refreshed the page

It only gives feedback on the first guess when you try to submit the second

It may not be checking bounds well. 

Changing the difficulty (range) doesn't reflect on the actual game, you are still asked to choose a number between 1 and 100 and the secrets are also still in the rang eof 1 to 100. it stays normal regardless of the setting

I don't think the ranges are intuitive for the levels of difficulty... but this may not be a serious bug.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| Guess of 20 | Hint == "Go higher" | Hint = "Go lower"| none|
|Guess of 30 | Hint == "Go lower" | Hint = "Go higher"| none |
|Difficulty =  Easy| "Guess a number between 1 and 20" | "Guess a number between 1 and 100" | none |

---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
I used Claude Code and Gemini
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
It suggested that I make the function update_score to equally penalize wrong guesses on both even and odd attempts (as the previous logic sometimes rewarded wrong guesses on even attempts with 5 points while always penalizing on odd ones).
I checked the code and saw that this was indeed true. I also tested it and experienced the glitch. I implemented the solutions Claude gave, and then the glitch was solved.
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).
When using Claude Haiku 4.5 in the chat, it said something about the backwards hints being caused by "string comparison on even attempts." 
It said that on even attempts, the secret is converted to a string while my guess remains an integer. Whne they try to get compared in check_guess(), a TypeError arises and falls back to string comparison. It stated "But string comparison s lexicographic, not numeric! So "9" > "100" is True, and feedback gets completely reversed."
This still doesn't really make sense to me, but upon looking at the referenced lines of code, I saw that the secret was unnecessarily converted to a string, so I took the conversion out.
Although I don't think this feedback is wrong (as it may be addressing some other issue), I just don't know how the "lexicographic" comparison caused that specific error (backwards feedback hints).
---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
When I could play the game and not experience the issue anymore
- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.
When I first ran the game manually, I noticed that the hints were backwards. So I looked into the code and saw that the logic was flipped, so I flipped them back.
- Did AI help you design or understand any tests? How?
It helped me understand that the test that were already given weren't going to pass due to a mismatch on return type expectations. It also helped me design additional tests to test the other fixes by giving me examples in the right format.
---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
Every time a user does anything on a Streamlit app, Streamlit throws away the entire page and re-runs the Python script from top to bottom.
The reason it doesn't appear to rerun all the time to a reset state is due to the session state. Streamlit keeps a session state that stores the state of the session so that things that need to reflect on multiple reruns can persist (until you decide to fully reset the session state).
---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
  Ensuring to verify AI outputs critically, treating it as a partner under your wing instead of some wise old sage. Taking control and leading the project rather than getting carried away by AI suggestions
  Also asking AI to write pytest cases for each change, and test them before committing.
- What is one thing you would do differently next time you work with AI on a coding task?
I would ask it to think thoroughly through it's answers and proposals before presenting them to me because keeping up with several suggestions is a bit too distracting.

- In one or two sentences, describe how this project changed the way you think about AI generated code.
I like how the project instructions walked me through how to think about my interaction with AI throughout the process. I know that it is also dependent on the context you give it and how detailed your prompt is.