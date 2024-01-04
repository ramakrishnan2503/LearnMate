import main 

def test_quiz_portion():
    # url = "https://www.youtube.com/watch?v=zsjvFFKOm3c&pp=ygUDc3Fs"
    data = '''Structured Query Language (SQL) is the standard language for communicating with relational database 
    management systems (RDBMS). It is used to manipulate data by reading, creating, updating, and deleting records. 
    SQL allows us to join data from different tables based on relationships. The syntax includes statements, keywords
    , and clauses like SELECT, WHERE, and JOIN. SQL is widely supported and used in technical applications. This 
    summary highlighted the key features and applications of SQL within the limit of 80 words.'''
    response = main.make_quiz(data=data)
    print(response)
    assert True
