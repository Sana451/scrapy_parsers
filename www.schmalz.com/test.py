def fu():
    asd = "asd"
    fff = 123
    ggg = 444
    yield (asd, fff, ggg)


data1, data2, data3 = fu()
print(data1, data2, data3)
