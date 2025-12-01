import spacy
import pandas as pd

# Load the small English model
nlp = spacy.load("en_core_web_sm")

def clean_and_split_text(text, team_data):
    """
    Custom logic to insert punctuation since Google STT often omits it.
    This helps spaCy split sentences correctly.
    """
    # 1. Get all team names
    names = [member['name'] for member in team_data]
    
    # 2. Define transition words that usually start a new sentence/task
    transitions = ["Also", "And", "But", "However", "We need", "We should", "One more thing"]
    
    # 3. Insert a period before these words if they appear
    # We use a temporary placeholder to avoid double periods
    for word in names + transitions:
        # Case insensitive replacement (e.g., " sakshi" -> ". Sakshi")
        text = text.replace(f" {word}", f". {word}")
        text = text.replace(f" {word.lower()}", f". {word}")
        
    return text

def extract_tasks_and_assign(text, team_data):
    # PRE-PROCESS: Fix the run-on sentence issue
    formatted_text = clean_and_split_text(text, team_data)
    
    doc = nlp(formatted_text)
    tasks = []
    
    # 1. Break text into sentences
    for sent in doc.sents:
        sent_text = sent.text.strip()
        
        # Skip empty or very short snippets (noise)
        if len(sent_text) < 10:
            continue
        
        # KEY LOGIC: Identify if a sentence is a task
        action_verbs = ["need", "fix", "create", "write", "design", "update", "optimize", "make", "tackle"]
        is_task = any(token.lemma_.lower() in action_verbs for token in sent)
        
        # Fallback: If it mentions a team member, it's likely a task assignment
        mentions_name = any(ent.label_ == "PERSON" for ent in sent.ents)
        
        if is_task or mentions_name:
            task_info = {
                "description": sent_text.replace(".", ""), # Clean up the dots we added
                "assignee": "Unassigned",
                "deadline": "Not specified",
                "priority": "Medium",
                "reason": "Skill match"
            }

            # 2. Extract Entities
            mentioned_names = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
            dates = [ent.text for ent in sent.ents if ent.label_ == "DATE"]
            
            if dates:
                task_info["deadline"] = dates[0]

            # 3. Determine Priority
            lower_text = sent_text.lower()
            if any(w in lower_text for w in ["critical", "urgent", "asap", "blocking", "high priority"]):
                task_info["priority"] = "High/Critical"
            elif any(w in lower_text for w in ["wait", "next week", "low"]):
                task_info["priority"] = "Low"

            # 4. Assign Task
            assigned = False
            
            # Logic A: Direct Mention
            for member in team_data:
                # Check if name is in the sentence text (more robust than spacy entity for lowercase)
                if member['name'].lower() in lower_text:
                    task_info['assignee'] = member['name']
                    task_info['reason'] = "Explicitly mentioned"
                    assigned = True
                    break
            
            # Logic B: Skill Matching
            if not assigned:
                best_match = None
                best_role = ""
                max_score = 0
                
                for member in team_data:
                    score = 0
                    for skill in member['skills']:
                        if skill.lower() in lower_text:
                            score += 1
                    
                    if score > max_score:
                        max_score = score
                        best_match = member['name']
                        best_role = member['role']
                
                if best_match:
                    task_info['assignee'] = best_match
                    task_info['reason'] = f"Matched skills ({best_role})"
                else:
                    task_info['assignee'] = "Team"
                    task_info['reason'] = "General task"

            tasks.append(task_info)

    return tasks

def save_to_csv(tasks, output_path):
    df = pd.DataFrame(tasks)
    if not df.empty:
        cols = ["description", "assignee", "priority", "deadline", "reason"]
        for col in cols:
            if col not in df.columns:
                df[col] = ""
        df = df[cols]
    
    df.to_csv(output_path, index=False)
    return df
