def pascal_to_snake(pascal: str) -> str:
    snake = ""
    for s in pascal:
        if s.isupper():
            snake = snake + "_"
        snake = snake + s.lower()
    return snake
