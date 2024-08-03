import re

def extract_session_id(session_str: str) -> str:
    match = re.search(r"/sessions/(.*?)/contexts/", session_str)
    if match:
        extracted_string = match.group(1)
        return extracted_string
    return ""
def get_string_from_food_dic(food_dict: dict):
    return ", ".join([f"{int(value)} {key}" for key, value in food_dict.items()])
if __name__ == "__main__":
    print(get_string_from_food_dic({"couscous":1,"pizza":2}))
