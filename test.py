import re
import sys

# text = "(3(3+4))(4)"

# pattern = re.compile(r'^\(*[0-9]+[\(\)]*([\+\-\*\/\^]?[\(\)]*[0-9]+[\(\)]*)*$')
# matches = pattern.finditer(text)

# for match in matches:
#     print(match.group())

string = "3.3"
pattern = re.compile(r'(\d+(\.\d+)?)')
matches = pattern.finditer(string)

# for match in matches:
#     print(match.group())
operators = re.findall(r'(\d+(?:\.\d+)?)', string)
print(operators)

sys.exit()

input = "3(3(4))(3)"

i = 0
start = 0
end = 0
start_found = False
end_found = False
start_extra = 0

while i < len(input) or not(start_found and end_found):
    if(input[i] == "("):
        if(not(start_found)):
            start = i
            start_found = True
        else:
            start_extra += 1

    if(input[i] == ")"):
        if(start_extra > 0):
            start_extra -= 1
        else:
            if(not(end_found)):
                end = i
                end_found = True

    i += 1

print(start)
print(end)

# paren_start = input.find("(")+1 
# paren_end = input.rfind(")")
# exp = input[paren_start:paren_end]

# print(exp)

