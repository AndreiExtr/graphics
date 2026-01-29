# график параболы на python
import matplotlib.pyplot as plt
import numpy as np

# сетка
plt.style.use('seaborn-v0_8-whitegrid')  # новый стиль seaborn
fig, ax=plt.subplots(2,2)

# графики
x = np.linspace(-1,1,10)
y=x**3
ax[0,0].plot(x,y,color="#167C34")

x = np.linspace(-10,10,100)
y=x**2
ax[1,0].plot(x,y)

x = np.linspace(-1,1,10)
y=x
ax[0,1].plot(x,y,color="#70167C")

x = np.linspace(-10,10,20)
y=np.sin(x)
ax[1,1].plot(x,y,color="#7C1616")

plt.show()

