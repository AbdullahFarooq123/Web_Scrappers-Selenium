def validate_error(error: int, limit: int):
    if error > limit:
        print('Internet Error')
        exit(1)