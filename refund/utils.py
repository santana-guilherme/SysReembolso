def is_member(user: object, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()

def is_analyst(user: object) -> bool:
    return user.groups.filter(name='Analyst').exists()

def is_treasurer(user: object) -> bool:
    return is_member(user, 'Treasurer')
