import google.generativeai as genai
import subprocess
import re

# Set your Gemini API key
API_KEY = 'AIzaSyC0PMNnSem09iSZUqiizGq0VxYoikHB-3I'

# Configure Gemini API
genai.configure(api_key=API_KEY)

# Use the correct model name
model = genai.GenerativeModel('gemini-1.5-flash')

# Start chat session
chat = model.start_chat(history=[])


def get_prompt():
    return input("Describe what you want to do in CMD: ").strip()


def ask_gem(prompt):
    instruction = (
        "I will describe what I want to do in Windows CMD. "
        "Reply ONLY with the exact command, no extra text, no explanations, no greetings. "
        "Respond with the command alone."
    )
    full_prompt = instruction + "\n" + prompt
    response = chat.send_message(full_prompt)
    gemini_output = response.text.strip()

    # Optional: Extract the command using regex to avoid any wrapping text
    cmd_match = re.search(r'`(.+?)`', gemini_output)  # If it returns Markdown-style code
    if cmd_match:
        command = cmd_match.group(1)
    else:
        command = gemini_output.strip()

    print(f"✅ Command: {command}")
    return command


def execute_command(command):
    print("🚀 Running the command...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("⚠️ Error:", result.stderr)
    except Exception as e:
        print("❌ Exception:", str(e))
    print("-" * 50)


# Main flow
if __name__ == "__main__":
    user_prompt = get_prompt()
    cmd_to_run = ask_gem(user_prompt)

    if cmd_to_run:
        execute_command(cmd_to_run)
    else:
        print("❗ No valid command received.")
