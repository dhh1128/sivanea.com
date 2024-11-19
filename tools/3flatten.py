import os
import re

for root, dirs, files in os.walk('.'):
    dirs[:] = [d for d in dirs if not d.startswith('_') and d != '.git']
    for file in files:
        if file == 'README': continue
        file_path = os.path.join(root, file)
        rel_path = os.path.relpath(file_path, '.')
        if file.endswith(''):
            pair = f'{rel_path} {file}'
        elif file.endswith('.png') or file.endswith('.jpg'):
            pair = f'{rel_path} assets/{file}'
        else:
            print(f'Ignoring {rel_path}')
            continue
        os.system('git mv ' + pair)

