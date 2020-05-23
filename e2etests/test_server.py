def test_example(selenium):
    selenium.get('http://web')
    assert 'HVZ' in selenium.title 
