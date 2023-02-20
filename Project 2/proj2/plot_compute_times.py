from matplotlib import pyplot as plt

x_values = []
y_values = []
avg_values = []

compute_times = open('compute_times.tsv', 'r').read()
compute_times = compute_times.splitlines()
for i in compute_times:
    i = i.split('\t')
    
    for j in i[1:-1]:
        x_values.append(int(i[0]))
        y_values.append(float(j))
    avg_values.append(float(i[-1]))

plt.scatter(x_values, y_values, s=1)
avg_x_values = []
for i in range(len(x_values)):
    if i % 5 == 0:
        avg_x_values.append(x_values[i])
plt.plot(avg_x_values, avg_values, color='red')
plt.show()
