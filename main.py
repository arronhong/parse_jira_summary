from bs4 import BeautifulSoup


with open('index.html') as f:
    soup = BeautifulSoup(f, 'html.parser')

out = open('out.txt', 'w')
bugs = ''

for table in soup.find_all(class_='tableBorder'):
    line = ''
    issue_href = table.find('h3', class_='formtitle').find('a')
    issue_title = issue_href.text
    if issue_title == 'Day off':
        continue

    issue_type = table.find_next_sibling('table').find('tr').select('td')[1].text.strip()
    if issue_type not in ['Sub-task', 'Task', 'Bug']:
        print(f'unexpected issue type: {issue_type}')
        continue

    ticket_number = issue_href.previous_sibling.text.strip()
    line += f'{ticket_number} '

    if issue_type == 'Sub-task':
        parent_title = table.find(id='parent_issue_summary').text
        line += f'{parent_title}，'
    line += f'{issue_title}\n'

    if issue_type == 'Bug':
        bugs += line
    else:
        out.write(line)

if bugs:
    out.write('\nbugs:\n')
    out.write(bugs)

out.close()
