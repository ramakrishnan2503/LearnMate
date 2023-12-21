from main import main, get_time_stamp

url = "https://www.youtube.com/watch?v=zsjvFFKOm3c&pp=ygUDc3Fs"
def test_main():
    response = main(url=url) 
    print(response)
    assert response != False


# def test_get_transcript():
#     print(get_time_stamp(url))
#     assert True