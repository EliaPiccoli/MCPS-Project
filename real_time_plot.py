import db
import matplotlib.pyplot as plt
from db import DBPATH

dev2pos = {
    'kitchen': (1230, 90),
    'bedroom1': (1235, 985),
    'bedroom2': (135, 1415),
    'bedroom3': (135, 720),
    'bathroom': (135, 565),
}

dbcon = db.create_connection(DBPATH)
img = plt.imread("images/casa_2.png")
plt.figure(figsize=(9, 8), dpi=100)
plt.subplots_adjust(0.037, 0, 1, 1)
while True:
    last_temp = db.get_last_temp(dbcon)
    plt.clf()
    plt.axis('off')
    plt.imshow(img)
    for t in last_temp:
        plt.annotate(f"{t[1]}", xy=dev2pos[t[0]])
    plt.show(block=False)
    plt.pause(1)
