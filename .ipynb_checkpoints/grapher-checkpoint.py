def parser(x, y):
    
    import matplotlib.pyplot as plt
    import statistics 
    
    
    data = open("times500.txt", "r")
    data = data.read()
    data1 = data.split("\t")
    data = data1[0]
    val = 0.0
    data = data.split(",")
        
    sus = []
    larger = []
    for i in range(0,x):
        for k in range(0,y):
            print(data[i+(x-1)*k])
            sus.append(float(data[i+(x-1)*k]))
        larger.append(statistics.stdev(sus))
    e = larger
    print(e)


    for i in range(0,x):
        print(data[i])
        for j in range(0,y):
            val += float(data[i*j])
        newarr.append((val/(x-1)))
    print(newarr)
    
    return([e, newarr, data1[1]])






def x_axis(x):
    matrix = []
    for i in range(0,x):
        matrix.append(pow(2,x))
    return matrixs
        