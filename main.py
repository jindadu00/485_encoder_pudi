import time
import matplotlib.pyplot as plt
from encoder import Encoder

print("Starting the encoder reading script...")

# Initialize encoder communication
encoder = Encoder()
print("Starting the encoder reading script...")

# Prepare plot
plt.ion()
fig, ax = plt.subplots()
y_data =[[],[],[],[],[],[],[],[],[]]


x_data = []
line=[]
line1, = ax.plot([], [], label='Encoder 1')
line2, = ax.plot([], [], label='Encoder 2')
line3, = ax.plot([], [], label='Encoder 3')
line4, = ax.plot([], [], label='Encoder 4')
line5, = ax.plot([], [], label='Encoder 5')
line6, = ax.plot([], [], label='Encoder 6')
line7, = ax.plot([], [], label='Encoder 7')
line8, = ax.plot([], [], label='Encoder 8')
line9, = ax.plot([], [], label='Encoder 9')
line.append(line1)
line.append(line2)
line.append(line3)
line.append(line4)
line.append(line5)
line.append(line6)
line.append(line7)
line.append(line8)
line.append(line9)


ax.set_ylim(0, 360)
ax.set_xlim(0, 50)
plt.legend()

ID=[1,2,3,4,5,6,7,8,9]
# for i in ID:
#     encoder.reset_encoder(i,2048)
#     time.sleep(0.1)


# Read angles in a loop and update plot
for i in range(5000):
    x_data.append(i)
    for k in ID:
        angle = encoder.read_angle(k)
        time.sleep(0.01)
        y_data[k-1].append(angle if angle is not None else 0)
        line[k-1].set_xdata(x_data)
        line[k-1].set_ydata(y_data[k-1])
    
    ax.set_xlim(max(0, i - 50), i + 1)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    # time.sleep(0.5)
    # print('y1_data',y1_data)
    # print('y2_data',y2_data)
    # print('y3_data',y3_data)



# Close the serial connection
encoder.close()
