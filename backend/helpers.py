


def paginate(list, page):
    QUESTIONS_PER_PAGE = 10
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    paginated_result = list[start:end]
    return paginated_result