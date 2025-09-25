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


# rule_based_recommend

def rule_based_recommend(user, internships, top_n=5):
    user_skills = set(skill.lower().strip() for skill in user.get("Skills", []))
    matched = []

    for row in internships:
        skills_raw = row.get("Required Skills") or row.get("RequiredSkills") or row.get("required_skills") or []
        
        # convert string to list if needed
        if isinstance(skills_raw, str):
            skills_list = [s.strip().lower() for s in skills_raw.split(",")]
        else:
            skills_list = [s.lower().strip() for s in skills_raw]

        match_skills = user_skills & set(skills_list)

        if match_skills:
            row["Skills_matched"] = list(match_skills)
            row["Score"] = len(match_skills)
            matched.append(row)

    matched.sort(key=lambda x: x["Score"], reverse=True)
    return matched[:top_n]             
