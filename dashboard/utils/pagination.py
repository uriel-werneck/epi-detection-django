from django.core.paginator import Page


def iter_pages(current_page: int, total: int, left_edge=1, right_edge=1, left_current=2, right_current=2) -> list:
    '''Returns a formated list of page numbers to display in pagination'''

    if current_page <= 0: current_page = 1
    if current_page > total: current_page = total

    range_list = list(range(1, total+1))
    
    # define left list
    left_part = range_list[:current_page-1]
    if current_page - left_current > left_edge + 1:
        left_part = [1, None] + list(range(current_page - left_current, current_page))

    # define right list
    right_part = range_list[current_page:total]
    if current_page + right_current < total - right_edge:
        right_part = list(range(current_page+1, current_page+right_current+1)) + [None, total]

    # define and return page list
    page_list = left_part + [current_page] + right_part
    return page_list


def get_detection_data(page_obj: Page) -> list[tuple[str, int]]:
    '''Returns a list of tuples containing detection objects and their class counts.'''

    detection_data = []

    for detection_object in page_obj:
        detected_classes = detection_object.detected_classes
        class_counts = []

        for class_name in set(detected_classes):
            class_counts.append((class_name, detected_classes.count(class_name)))
        
        detection_data.append((detection_object, class_counts))
    
    return detection_data