#class Solution:
#    def romanToInt(self, s: str) -> int:
s="MCMXCIV"
roman_dict={'I':1, 'V':5,'X':10,'L':50, 'C':100, 'D':500,'M':1000}
except_dict={'IV':4, 'IX':9, 'XL':40, 'XC':90, 'CD':400, 'CM':900}
#combined_dict = {**roman_dict, **except_dict}
#original_string=s
num=0
found_exceptions  = []

for x in except_dict.keys():
    if x in s:
        found_exceptions.append(x)
        s.replace(x,"")
        print(s)

#if len(s)!=0
#    found_exceptions.append(s)

for y in found_exceptions:
    n= [value for k, value in except_dict.items() if y==k]
    num += n[0]

#if s not in except_dict.keys():
if len(s)!=0:
    roman_list=list(s)
    for r_num in roman_list:
        n = [value for k, value in roman_dict.items() if r_num==k]
        num += n[0]
#else:
#    num = [value for k, value in except_dict.items() if s==k]
  
