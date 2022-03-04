from email.mime import image
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageFile, ImageColor

img = Image.open("C:/Users/Administrator/Desktop/Zen Baboon - Hidden Frogs/cover.jpg")
b = ImageColor.getcolor("blue", "L")
ai = np.asarray(img)


plt.subplot(1,5,1)
orin = Image.fromarray(ai[:,:, [0,1,2]])
plt.imshow(orin)

plt.subplot(1,5,2)
r = Image.fromarray(ai[:, :, 0] )
plt.imshow(r)


plt.subplot(1,5,3)
b = Image.fromarray(ai[:, :, 1] )
plt.imshow(b)

plt.subplot(1,5,4)
g = Image.fromarray(ai[:,:, 2])
plt.imshow(g)

plt.subplot(1,5,5)
plt.title("Blue C0's color show in Plot")
plt.plot(ai[0,:, 2])


plt.show()