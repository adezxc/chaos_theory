import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def julia_set(f, xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    img = np.zeros(Z.shape, dtype=float)
    ix, iy = np.indices(Z.shape)

    for i in range(max_iter):
        mask = np.abs(Z) < 1000
        Z[mask] = f(Z[mask])
        img[ix[mask], iy[mask]] += 1

    return img

def mandelbrot(f, xmin, xmax, ymin, ymax, width, height, max_iter):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Lambda = X + 1j * Y
    Z = np.zeros_like(Lambda)

    img = np.zeros(Z.shape, dtype=float)
    ix, iy = np.indices(Z.shape)

    for i in range(max_iter):
        mask = np.abs(Z) < 1000
        Z[mask] = f(Z[mask], Lambda[mask])
        img[ix[mask], iy[mask]] += 1

    return img

root = tk.Tk()
root.title("Interactive Mandelbrot and Julia Sets")

fig1, ax1 = plt.subplots(figsize=(6, 6))
fig2, ax2 = plt.subplots(figsize=(6, 6))
fig_newton, ax_newton = plt.subplots(figsize=(6, 6))

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas_widget1 = canvas1.get_tk_widget()
canvas_widget1.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

canvas2 = FigureCanvasTkAgg(fig2, master=root)
canvas_widget2 = canvas2.get_tk_widget()
canvas_widget2.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

canvas_newton = FigureCanvasTkAgg(fig_newton, master=root)
canvas_widget_newton = canvas_newton.get_tk_widget()
canvas_widget_newton.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

lambda_value = 0.7885
f = lambda z: lambda_value * z**3 + z**2 + lambda_value
f_prime = lambda z: 3 * lambda_value * z**2 + 2 * z

fig, ax = plt.subplots()
fig.xmin, fig.xmax, fig.ymin, fig.ymax = -1.5, 1.5, -1.5, 1.5
width, height = 800, 800
max_iter = 300

def newton_fractal(f, f_prime, xmin, xmax, ymin, ymax, width, height, max_iter, tol):
    x = np.linspace(xmin, xmax, width)
    y = np.linspace(ymin, ymax, height)
    X, Y = np.meshgrid(x, y)
    Z = X + 1j * Y

    img = np.zeros(Z.shape, dtype=int)

    for i in range(max_iter):
        Z_prime = f(Z)
        delta = Z_prime / f_prime(Z)
        Z -= delta
        mask = np.abs(delta) < tol
        img[mask] = i

    return img

# Update function for Newton fractal
def update_newton(xmin, xmax, ymin, ymax):
    newton_img = newton_fractal(f, f_prime, xmin, xmax, ymin, ymax, width, height, max_iter, tolerance)
    ax_newton.clear()
    ax_newton.imshow(newton_img, extent=[xmin, xmax, ymin, ymax], cmap='hot', origin='lower')
    canvas_newton.draw()

# Event handler for Newton fractal clicks

def update_julia(cx, cy):
    lambda_value = 0.7885
    f = lambda z: lambda_value * z**3 + z**2 + lambda_value + complex(cx, cy)
    julia_img = julia_set(f, fig2.xmin, fig2.xmax, fig2.ymin, fig2.ymax, width, height, max_iter)
    ax2.clear()
    ax2.imshow(julia_img, extent=[fig2.xmin, fig2.xmax, fig2.ymin, fig2.ymax], cmap='hot', origin='lower')
    canvas2.draw()

def update_mandelbrot():
    f = lambda z, lambda_value: lambda_value * z**3 + z**2 + lambda_value
    mandelbrot_img = mandelbrot(f, fig1.xmin, fig1.xmax, fig1.ymin, fig1.ymax, width, height, max_iter)
    ax1.clear()
    ax1.imshow(mandelbrot_img, extent=[fig1.xmin, fig1.xmax, fig1.ymin, fig1.ymax], cmap='hot', origin='lower')
    canvas1.draw()

def on_click_julia(event):
    if event.dblclick and event.inaxes:
        x, y = event.xdata, event.ydata
        dx, dy = (fig2.xmax - fig2.xmin) / 4, (fig2.ymax - fig2.ymin) / 4
        fig2.xmin, fig2.xmax = x - dx, x + dx
        fig2.ymin, fig2.ymax = y - dy, y + dy
        update_julia(fig2.cx, fig2.cy)

def on_click_mandelbrot(event):
    if event.dblclick and event.inaxes:
        x, y = event.xdata, event.ydata
        dx, dy = (fig1.xmax - fig1.xmin) / 4, (fig1.ymax - fig1.ymin) / 4
        fig1.xmin, fig1.xmax = x - dx, x + dx
        fig1.ymin, fig1.ymax = y - dy, y + dy
        update_mandelbrot()
        update_julia(x,y)

def on_click_newton(event):
    if event.dblclick and event.inaxes:
        x, y = event.xdata, event.ydata
        dx, dy = (fig_newton.xmax - fig_newton.xmin) / 4, (fig_newton.ymax - fig_newton.ymin) / 4
        fig_newton.xmin, fig_newton.xmax = x - dx, x + dx
        fig_newton.ymin, fig_newton.ymax = y - dy, y + dy
        update_newton(fig_newton.xmin, fig_newton.xmax, fig_newton.ymin, fig_newton.ymax)

fig1.canvas.mpl_connect('button_press_event', on_click_mandelbrot)
fig1.xmin, fig1.xmax, fig1.ymin, fig1.ymax = -2, 2, -2, 2
fig2.canvas.mpl_connect('button_press_event', on_click_julia)
fig_newton.canvas.mpl_connect('button_press_event', on_click_newton)
fig2.xmin, fig2.xmax, fig2.ymin, fig2.ymax = -1.5, 1.5, -1.5, 1.5
fig2.cx, fig2.cy = 0, 0  # Initial seed for the Julia set
fig_newton.xmin, fig_newton.xmax, fig_newton.ymin, fig_newton.ymax = -2, 2, -2, 2
tolerance = 1e-6

# Initial plots
update_mandelbrot()
update_julia(0, 0)
update_newton(-2,2,-2,2)

root.mainloop()
