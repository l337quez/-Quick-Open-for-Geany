import re


def get_pattern(what):
    parts = what.split('/')

    if len(parts) <= 1:
        return None

    rexp = r'(/|^)' + r'[^/]+/'.join(map(re.escape, parts))
    return re.compile(rexp)


def name_start_match(what):
    def inner(name, path):
        return name.startswith(what)

    return inner


def name_match(what):
    def inner(name, path):
        return what in name

    return inner


def path_match(what):
    def inner(name, path):
        return what in path

    return inner


def fuzzy_match(what):
    pattern = get_pattern(what)

    def inner(name, path):
        if pattern:
            return pattern.search(path) is not None
        else:
            return False

    return inner


def dir_is_good(name, path):
    if name.startswith('.'):
        return False

    return True


def file_is_good(name, path):
    is_good = (not any(map(name.endswith, ('.pyc', '.pyo', '.png')))
                and not name.startswith('.'))
    return is_good


def search(root, top, match, already_matched, tick):
    from os import listdir
    from os.path import join, isdir

    tick()

    dirs_to_visit = []
    for name in listdir(join(root, top)):
        tick()
        fullpath = join(root, top, name)
        path = join(top, name)

        if isdir(fullpath):
            if dir_is_good(name, path):
                dirs_to_visit.append(path)
        elif ((name, top) not in already_matched
            and match(name, path)
            and file_is_good(name, path)):
            yield name, top

    for path in dirs_to_visit:
        for p in search(root, path, match, already_matched, tick):
            yield p
