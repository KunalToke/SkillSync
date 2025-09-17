# models/roadmap.py
def get_user_roadmap_progress(username):
    """
    Example logic:
    - Fetch user's roadmap milestones from DB
    - Count completed vs total
    """
    # Example static data — replace with DB queries
    milestones = [
        {"name": "Complete Resume", "done": True},
        {"name": "Build Portfolio", "done": False},
        {"name": "Finish AI Course", "done": True},
        {"name": "Mock Interviews", "done": False},
    ]
    total = len(milestones)
    done = len([m for m in milestones if m["done"]])
    if total == 0:
        return 0
    return int((done / total) * 100)
