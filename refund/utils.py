def is_member(user: object, group_name: str) -> bool:
    return user.groups.filter(name=group_name).exists()

def is_analyst(user: object) -> bool:
    return is_member(user, 'Analyst')

def is_treasurer(user: object) -> bool:
    return is_member(user, 'Treasurer')


def its_only(user: object, group_name: str) -> bool:
    return is_member(user, group_name) and len(user.groups.all()) == 1
