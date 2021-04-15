# this function receives a datetime object and converts it to a string formatted as month/day/year
def format_date(date):
  return date.strftime('%m/%d/%y')

# this function receives a url and returns the domain name
def format_url(url):
  return url.replace('http://', '').replace('https://', '').replace('www.', '').split('/')[0].split('?')[0]

# this function receives an amount and a word. returns plural if amount > 1
def format_plural(amount, word):
  if amount != 1:
    return word + 's'
  
  return word
