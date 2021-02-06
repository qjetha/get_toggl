import tkinter as tk
from get_toggl import get_toggl_data
from tkinter import filedialog
from tkinter import messagebox

folder_selected = str()

def main():
	master = tk.Tk()
	master.geometry("450x200")
	master.title('Extract Toggl Data')

	# Label for Workstream
	select_label = tk.Label(master, text="Select details about the export:")
	select_label.grid(row=0, column=0, padx=10, sticky="W")

	# Select the Dates
	tk.Label(master, text="Start Date (YYYY-MM-DD):").grid(row=3, column=0, pady=10, padx=10, sticky="W")
	tk.Label(master, text="End Date (YYYY-MM-DD):").grid(row=4, column=0, padx=10, sticky="W")

	start = tk.Entry(master)
	end = tk.Entry(master)
	start.grid(row=3, column=0, padx=200)
	end.grid(row=4, column=0, padx=200)


	def dialog_box():
		global folder_selected
		folder_selected = filedialog.askdirectory()

	button = tk.Button(master, text="Select Directory", width=40, command=dialog_box)
	button.grid(row=5, column=0, sticky="W", pady=20, padx=40)


	def run():
		error = 0
		if start.get() == 0 or end.get() == 0:
			error=1
			tk.messagebox.showinfo(title="Error", message="Must specify either both a start and end date.")
		if folder_selected=="":
			error=1
			tk.messagebox.showinfo(title="Error", message="Must specify an output directory.")

		if error==0:
			get_toggl_data(start.get(), end.get(), folder_selected)

	button = tk.Button(master, text="Extract Data", width=10, fg="blue", command=run)
	button.grid(row=8, column=0, sticky="W", pady=10, padx=180)

	master.mainloop()


if __name__=="__main__":
	main()
	