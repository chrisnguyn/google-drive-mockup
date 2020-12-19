# remove duplicate tags entered under one photo
def clean_tags(caption):
    if caption == None or len(caption) == 0:
        return None

    ret = []
    seen = set()

    for word in caption.split(' '):
        if word not in seen:
            ret.append(word)
            ret.append(' ')
            seen.add(word)

    return ''.join(ret)


# get top three tags used
def get_top_tags(files):
    if files == None or len(files) == 0:
        return None

    tags = {}

    for file in files:
        for tag in file.tag.split(' '):
            if tag == 'NO_TAG' or tag == '':
                continue
            elif tag not in tags:
                tags[tag] = 0
            tags[tag] += 1

    return sorted(tags.items(), key=lambda x: x[1], reverse=True)
