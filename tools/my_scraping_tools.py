from http.cookies import SimpleCookie
import csv


def save_error(url, error, field, err_file_path):
    with open(err_file_path, "a") as error_csvfile:
        writer = csv.writer(error_csvfile)
        writer.writerow([url, field, type(error), error])


def cookie_dict_from_string(raw_cookie_str: str) -> dict:
    cookie = SimpleCookie()
    cookie.load(raw_cookie_str)
    cookies = {k: v.value for k, v in cookie.items()}
    return cookies
