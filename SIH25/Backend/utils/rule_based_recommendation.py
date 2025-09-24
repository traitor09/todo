from utils.preprocess import normalize_eligibility, preprocess_degree

def is_eligible(user_input: str, internship_eligibility: str) -> bool:
    user_norm = normalize_eligibility(user_input)
    intern_norm = normalize_eligibility(internship_eligibility)

    if not intern_norm:  
        return True  # internship didn’t specify → open to all

    if intern_norm == "1": return user_norm == "1"
    if intern_norm == "2": return user_norm == "2"
    if intern_norm == "3": return user_norm == "3"
    if intern_norm == "4": return user_norm == "4"
    if intern_norm == "UG": return user_norm in ["1", "2", "3", "4", "UG"]
    if intern_norm == "PG": return user_norm in ["PG"]

    return False



def rule_based_recommend(user, internships, top_n=5):
    user_skills = set(skill.lower().strip() for skill in user.get("Skills", []))
    print("User Skills:", user_skills)

    matched = []

    for row in internships:
        intern_skills = set(skill.lower().strip() for skill in row.get("Required Skills_processed", []))
        print(f"\nChecking: {row.get('Title', 'No Title')}")
        print("Internship Skills:", intern_skills)

        match_skills = user_skills & intern_skills
        print("Matched Skills:", match_skills)

        if match_skills:
            row["Skills_matched"] = list(match_skills)
            row["Score"] = len(match_skills)
            matched.append(row)

    matched.sort(key=lambda x: x["Score"], reverse=True)
    print(f"\nTotal Matches Found: {len(matched)}")
    return matched[:top_n]

             
