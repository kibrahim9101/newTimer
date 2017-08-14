import logging
import Tkinter as tk
import time
from pygame import mixer

log_format = '%(asctime)-6s: %(name)s - %(levelname)s - %(message)s'
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(log_format))
logger= logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(console_handler)



class timerUI(tk.Tk):
	def __init__(self, *args, **kwargs):
		tk.Tk.__init__(self, *args, **kwargs)
		self.minsize(width=800, height=400)
		self.maxsize(width=800, height=400)
		container = tk.Frame(self)
		container.pack(side="top", fill="both", expand=True)
		container.grid_rowconfigure(0, weight=1)
		container.grid_rowconfigure(2, weight=1)
		container.grid_columnconfigure(0, weight=1)
		container.grid_columnconfigure(2, weight=1)
		mixer.init()
		self.airRaid = mixer.Sound('airraid.wav')
		self.hours = tk.IntVar()
		self.minutes = tk.IntVar()
		self.seconds = tk.IntVar()
		self.armCode = tk.StringVar()
		self.disarmCode = tk.StringVar()
		self.total = tk.IntVar()
		self.timer = tk.StringVar()
		self.tick = None
		self.frames = {}
		for F in (armPage, timerPage):
			page_name = F.__name__
			frame = F(parent=container, controller=self)
			self.frames[page_name] = frame
			frame.grid(row=1, column=1, sticky="nsew")
			
		self.show_frame("armPage")

	def show_frame(self, page_name):
		frame = self.frames[page_name]
		frame.tkraise()

	def totalSeconds(self):
		hours = self.hours.get()
		minutes = self.minutes.get()
		seconds = self.seconds.get()
		total = hours * 3600 + minutes * 60 + seconds
		self.total.set(total)
		#self.tick = self.after(1000, self.countdown)

	def countdown(self):
		self.tick = self.after(1000, self.countdown)
		total = self.total.get()
		m, s = divmod(total, 60)
		h, m = divmod(m, 60)
		countdownString = "%02d:%02d:%02d" % (h, m, s)
		self.timer.set(countdownString)
		if (total == 0):
			self.after_cancel(self.tick)
			self.siren()
		elif (total > 0):
			total = total - 1
			self.total.set(total)
			self.tick
	def siren(self):
		self.airRaid.play(0)
		

class armPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent, width=800, height=400)
		self.controller = controller
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.hrLabel = tk.Label(self, text="Hours", anchor='w')
		self.hrLabel.grid(row=0, column=0, sticky='w')
		self.minLabel = tk.Label(self, text="Minutes")
		self.minLabel.grid(row=1, column=0, sticky='w')
		self.secLabel = tk.Label(self, text="Seconds")
		self.secLabel.grid(row=2, column=0, sticky='w')
		self.codeLabel = tk.Label(self, text="Disarm Code")
		self.codeLabel.grid(row=3, column=0, sticky='w')
		self.hrBox = tk.Entry(self, textvariable=self.controller.hours)
		self.hrBox.grid(row=0, column=1, sticky='e')
		self.minBox = tk.Entry(self, textvariable=self.controller.minutes)
		self.minBox.grid(row=1, column=1, sticky='e')
		self.secBox = tk.Entry(self, textvariable=self.controller.seconds)
		self.secBox.grid(row=2, column=1, sticky='e')
		self.codeBox = tk.Entry(self, textvariable=self.controller.armCode)
		self.codeBox.grid(row=3, column=1, sticky='e')
		self.armButton = tk.Button(self, text="Arm Bomb",
									command=self.getValues)
		self.armButton.grid(row=4, column=1, sticky='e')

	def getValues(self):
		self.controller.hours.get()
		self.controller.minutes.get()
		self.controller.seconds.get()
		self.controller.armCode.get()
		self.controller.totalSeconds()
		self.controller.show_frame("timerPage")
		self.controller.countdown()

class timerPage(tk.Frame):
	def __init__(self, parent, controller):
		tk.Frame.__init__(self, parent, width=800, height=400)
		self.controller = controller
		self.errorMessage = tk.StringVar()
		self.grid()
		self.createWidgets()

	def createWidgets(self):
		self.timerLabel = tk.Label(self, textvariable=self.controller.timer, font=('Helvetica', 18))
		self.timerLabel.grid(row=0, column=0)
		self.disarmBox = tk.Entry(self, textvariable=self.controller.disarmCode)
		self.disarmBox.grid(row=1, column=0)
		self.disarmButton = tk.Button(self, text="Disarm", command=self.disarmBomb)
		self.disarmButton.grid(row=2, column=0)
		self.errorLabel = tk.Label(self, textvariable=self.errorMessage)
		self.errorLabel.grid(row=3, column=0)

	def disarmBomb(self):
		arm = self.controller.armCode.get()
		disarm = self.controller.disarmCode.get()
		if (disarm == arm):
			self.controller.after_cancel(self.controller.tick)
			self.controller.airRaid.stop()
			self.controller.total.set(0)
			self.controller.show_frame("armPage")
		else:
			self.errorMessage.set("ERROR!")

	
		
	

newBomb = bombUI()
newBomb.mainloop()
		
