This is the protoytype for our Voice Agent Chatbot. Due to sound technical issues in Windows and WSL, this program must be runned on Linux/MacOS system.

For the .env file, you will need three APIs:
(1) AssemblyAI API for transcriber (speech to text)
(2) OPENAI API for prompting a response
(3) ELEVENLABS API for text to speech

First, run all the commands in instructions.md in your terminal. Then, create account and make three APIs keys in the env_example file. 

Then run this command to run the program

```bash
python ai.py
```
or 
```bash
python3 ai.py
```

In the future, we will merge this with our current NomNom Chat Bot [here](https://github.com/PhucNguyen-rsc/NomNomChatBot).