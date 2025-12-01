import json
import os
from transcriber import transcribe_audio
from processor import extract_tasks_and_assign, save_to_csv

def main():
    print("=== Meeting Task Assigner System ===")
    
    # Configuration Paths
    AUDIO_FILE = os.path.join("data", "input_audio.wav") 
    TEAM_FILE = os.path.join("data", "team_members.json")
    OUTPUT_FILE = os.path.join("output", "task_assignments.csv")

    # 1. Load Team Data
    if not os.path.exists(TEAM_FILE):
        print(f"CRITICAL ERROR: {TEAM_FILE} not found.")
        return

    with open(TEAM_FILE, 'r') as f:
        team_data = json.load(f)

    # 2. Transcribe Audio
    # We check if the file exists. If not, we use the text from the PDF for demonstration.
    if os.path.exists(AUDIO_FILE):
        print(f"Audio file found: {AUDIO_FILE}")
        transcribed_text = transcribe_audio(AUDIO_FILE)
    else:
        print(f"Warning: {AUDIO_FILE} not found.")
        print("Using SAMPLE TEXT from Project PDF for demonstration purposes...")
        transcribed_text = """
        Hi everyone, let's discuss this week's priorities. 
        Sakshi, we need someone to fix the critical login bug that users reported yesterday. 
        This needs to be done by tomorrow evening since it's blocking users. 
        Also, the database performance is really slow, Mohit you're good with backend optimization right? 
        We should tackle this by end of this week, it's affecting the user experience. 
        And we need to update the API documentation before Friday's release this is high priority. 
        Oh, and someone should design the new onboarding screens for the next sprint. 
        Arjun, didn't you work on UI designs last month? This can wait until next Monday. 
        One more thing we need to write unit tests for the payment module. 
        """

    print(f"\n--- Transcribed Text ---\n{transcribed_text}\n------------------------\n")

    # 3. Process Logic
    print("Analyzing text and matching skills...")
    tasks = extract_tasks_and_assign(transcribed_text, team_data)

    # 4. Save Output
    if tasks:
        df = save_to_csv(tasks, OUTPUT_FILE)
        print("\nSUCCESS! Task assignments generated:")
        print(df.to_string())
        print(f"\nResults saved to: {OUTPUT_FILE}")
    else:
        print("No tasks identified in the text.")

if __name__ == "__main__":
    main()
