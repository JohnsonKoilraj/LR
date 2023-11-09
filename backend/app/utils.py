
from app.core.config import settings
import math


def pagination(row_count=0, page = 1, size=10):
    current_page_no = page if page >= 1 else 1

    total_pages = math.ceil(row_count / size)

    if current_page_no > total_pages:
        current_page_no = total_pages
    
    limit =  current_page_no * size
    offset = limit - size

    if limit > row_count:
        limit = offset + (row_count % size)
    
    limit = limit - offset

    if offset < 0:
        offset = 0
    
    return [limit, offset]

def new_pagination(row_count=0, page = 1, size=10):
    current_page_no = page if page >= 1 else 1

    total_pages = math.ceil(row_count / size)

    if current_page_no > total_pages:
        current_page_no = total_pages
        return [0,0]
    limit =  current_page_no * size
    offset = limit - size

    if limit > row_count:
        limit = offset + (row_count % size)
    
    limit = limit - offset

    if offset < 0:
        offset = 0
    
    return [limit, offset]


def paginate(page, size, data, total):
    reply = {"items": data, "total":total, "page": page, "size":size}
    return reply
def paginate_for_file_count(page, size, data, total,file_count):
    reply = {"items": data, "total":total, "page": page,"file_count":file_count, "size":size}
    return reply

