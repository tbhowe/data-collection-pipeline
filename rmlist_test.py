my_list=[1,2,[33,00],4,6,"string",[444, 556],7]

filtered=[x for x in my_list if not isinstance(x, list)]
print(filtered)