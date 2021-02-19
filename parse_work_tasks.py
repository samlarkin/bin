from subprocess import check_output

with open('todo.txt', 'r') as f:
    text = f.readlines()
    text = text[1:]

for line in text:
    (pro, desc) = tuple(line.strip().split(maxsplit=1))
    check_output(['task', 'add', f'pro:{pro}', f'{desc}', '+@work'])

print(f'{len(text)} tasks added from work todo.txt')
