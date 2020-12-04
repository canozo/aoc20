import re
import sys

def redirect_stdout(filename = 'logs.txt'):
    open(filename, 'w').close()
    sys.stdout = open(filename, 'w')

passports = []

unflagged_passport = {
    'byr': False,
    'iyr': False,
    'eyr': False,
    'hgt': False,
    'hcl': False,
    'ecl': False,
    'pid': False,
    'cid': False
}

empty_passport = {
    'byr': None,
    'iyr': None,
    'eyr': None,
    'hgt': None,
    'hcl': None,
    'ecl': None,
    'pid': None,
    'cid': None
}

def is_valid(passport):
    return passport['byr'] and passport['iyr'] and passport['eyr'] and passport['hgt'] and passport['hcl'] and passport['ecl'] and passport['pid']

def is_valid_v2(passport):
    # check if any of the fields is None
    if passport['byr'] is None or passport['iyr'] is None or passport['eyr'] is None or passport['hgt'] is None or passport['hcl'] is None or passport['ecl'] is None or passport['pid'] is None:
        return False

    # check every field one by one
    byr = 1920 <= int(passport['byr']) <= 2002
    iyr = 2010 <= int(passport['iyr']) <= 2020
    eyr = 2020 <= int(passport['eyr']) <= 2030
    hcl = re.match('^#[0-9a-f]{6}$' , passport['hcl']) is not None
    ecl = passport['ecl'] in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']
    pid = re.match('^[0-9]{9}$', passport['pid']) is not None

    # check height here because I hate ternary
    hgt = False
    if 'cm' in passport['hgt']:
        hgt = 150 <= int(passport['hgt'][:len(passport['hgt']) - 2]) <= 193
    elif 'in' in passport['hgt']:
        hgt = 59 <= int(passport['hgt'][:len(passport['hgt']) - 2]) <= 76

    print(f"""
byr ({passport['byr']}) => {byr}
iyr ({passport['iyr']}) => {iyr}
eyr ({passport['eyr']}) => {eyr}
hgt ({passport['hgt']}) => {hgt}
hcl ({passport['hcl']}) => {hcl}
ecl ({passport['ecl']}) => {ecl}
pid ({passport['pid']}) => {pid}
""")

    return byr and iyr and eyr and hgt and hcl and ecl and pid

def v1(input_file):
    with open(input_file, 'r') as file:
        passport_fields = unflagged_passport.copy()

        for line in file.readlines():
            if line == '\n':
                # check if passport_fields contains all the needed fields
                if (is_valid(passport_fields)):
                    passports.append(passport_fields)

                # reset passport
                passport_fields = unflagged_passport.copy()
                print('-------------------------------')

            for field in line.strip('\n').split(' '):
                if field == '\n':
                    break
                if field == '':
                    continue
                [key, value] = field.split(':')
                print('- ' + key + ' => ' + value)
                passport_fields[key] = True

        # check if last remaining passport_fields contains all the needed fields
        if (is_valid(passport_fields)):
            passports.append(passport_fields)
        print('-------------------------------')

    print(f'Valid passports: {len(passports)}')

def v2(input_file):
    with open(input_file, 'r') as file:
        passport_fields = empty_passport.copy()

        for line in file.readlines():
            if line == '\n':
                # check if passport_fields contains all the needed fields
                if (is_valid_v2(passport_fields)):
                    passports.append(passport_fields)

                # reset passport
                passport_fields = empty_passport.copy()
                print('-------------------------------')

            for field in line.strip('\n').split(' '):
                if field == '\n':
                    break
                if field == '':
                    continue
                [key, value] = field.split(':')
                print('- ' + key + ' => ' + value)
                passport_fields[key] = value

        # check if last remaining passport_fields contains all the needed fields
        if (is_valid_v2(passport_fields)):
            passports.append(passport_fields)
        print('-------------------------------')

    print(f'Valid passports: {len(passports)}')

redirect_stdout()

# v1('input.txt')
# v1('example.txt')

v2('input.txt')
# v2('example.txt')

