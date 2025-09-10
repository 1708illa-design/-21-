a=[21,2,31,42,53,67,72,18,93,11,'яблуко','вишня', 'груша', 'апельсин', 'слива', 'виноград', 'ананас', 'ківі', 'манго', 'персик']
nums = []#список числ
words = []#список слів
for el in a:
    if type(el) == int:
        nums.append(el)
    else:
        words.append(el)
nums.sort()
words.sort()
list = nums + words
even_list = []
for n in nums:
    if n % 2 == 0:
        even_list.append(n)
caps_list = []
for w in words:
        caps_list.append(w.upper())
print("Перший список",a)
print("Відсортований список ",list)
print("Парні числа ",even_list)
print("Капс ",caps_list)