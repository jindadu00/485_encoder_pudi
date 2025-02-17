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
x_data, y1_data, y2_data, y3_data = [], [], [], []
line1, = ax.plot([], [], label='Encoder 1')
line2, = ax.plot([], [], label='Encoder 2')
line3, = ax.plot([], [], label='Encoder 3')
ax.set_ylim(0, 360)
ax.set_xlim(0, 50)
plt.legend()

# Read angles in a loop and update plot
for i in range(50):
    angle1 = encoder.read_angle(1)
    time.sleep(0.01)

    angle2 = encoder.read_angle(2)
    time.sleep(0.01)

    angle3 = encoder.read_angle(3)
    time.sleep(0.01)
    
    x_data.append(i)
    y1_data.append(angle1 if angle1 is not None else 0)
    y2_data.append(angle2 if angle2 is not None else 0)
    y3_data.append(angle3 if angle3 is not None else 0)
    
    # Update plot data
    line1.set_xdata(x_data)
    line1.set_ydata(y1_data)
    line2.set_xdata(x_data)
    line2.set_ydata(y2_data)
    line3.set_xdata(x_data)
    line3.set_ydata(y3_data)
    
    ax.set_xlim(max(0, i - 50), i + 1)
    fig.canvas.draw()
    fig.canvas.flush_events()
    
    time.sleep(0.5)
    # print('y1_data',y1_data)
    # print('y2_data',y2_data)
    # print('y3_data',y3_data)



# Close the serial connection
encoder.close()
