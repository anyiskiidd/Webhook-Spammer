import sys
import time
import os
import requests
import tkinter as tk
from colorama import Fore, init


class WebhookSpam:
    def __init__(self):
        pass
    
    def start(self):
        self.root = tk.Tk()
        self.root.title('Webhook Spam')

        self.label1 = tk.Label(self.root, text="Choose an option:")
        self.label1.pack()

        self.choice_var = tk.IntVar()
        self.choice_var.set(1)
        self.choice1 = tk.Radiobutton(self.root, text="Spam webhook", variable=self.choice_var, value=1)
        self.choice2 = tk.Radiobutton(self.root, text="Delete webhook", variable=self.choice_var, value=2)
        self.choice1.pack()
        self.choice2.pack()

        self.label2 = tk.Label(self.root, text="Webhook:")
        self.label2.pack()

        self.webhook_var = tk.StringVar()
        self.webhook_entry = tk.Entry(self.root, textvariable=self.webhook_var)
        self.webhook_entry.pack()

        self.label3 = tk.Label(self.root, text="Message:")
        self.label3.pack()

        self.message_var = tk.StringVar()
        self.message_entry = tk.Entry(self.root, textvariable=self.message_var)
        self.message_entry.pack()

        self.label4 = tk.Label(self.root, text="Iterations:")
        self.label4.pack()

        self.iterations_var = tk.IntVar()
        self.iterations_entry = tk.Entry(self.root, textvariable=self.iterations_var)
        self.iterations_entry.pack()

        self.button = tk.Button(self.root, text="Start", command=self.on_button_click)
        self.button.pack()

        self.textbox = tk.Text(self.root)
        self.textbox.pack()

        self.root.mainloop()

    def on_button_click(self):
        choice = self.choice_var.get()
        webhook = self.webhook_var.get()
        message = self.message_var.get()
        iterations = self.iterations_var.get()

        if choice not in [1, 2]:
            self.print_message(f"{Fore.RED}Invalid Choice!") 
            self.exit()

        if choice == 1:
            if not self.check_webhook(webhook): 
                self.print_message(f"{Fore.RED}Invalid Webhook!{Fore.RESET}")
                self.exit()

            if iterations < 0:
                self.print_message(f"{Fore.RED}Invalid Iterations!{Fore.RESET}")
                self.exit()

            self.spam_threads(webhook, self.inflate_message(message), iterations)

        if choice == 2:
            self.print_message(f"{Fore.GREEN}Deleting Webhook!{Fore.RESET}")
            requests.delete(webhook)
            self.print_message(f"{Fore.GREEN}Webhook has been deleted!{Fore.RESET}") 
            self.exit()

    def spam_threads(self, webhook, message, iterations):
        def spam(webhook, message):
            r = requests.post(
                webhook,
                json={"content": message}
            )
            
            if r.status_code == 204:
                self.print_message(f"{Fore.GREEN}Sent! | {r.status_code}\n{Fore.RESET}")
                
            elif r.status_code == 429:
                self.print_message(f"{Fore.RED}Rate Limit! | {r.status_code}\n{Fore.RESET}")
                return 429
                
            else:
                self.print_message(f"{Fore.YELLOW}{r.status_code}\n{Fore.RESET}")
                self.exit()
        
        message = self.inflate_message(message)
                
        for x in range(iterations):
            for _ in range(5):
                if spam(webhook, message) == 429:
                    time.sleep(5)
                
            time.sleep(5)
            
        self.exit()

    def inflate_message(self, message):
        message = f"@everyone {message}\n"
        message = message * (999//len(message) + 1)
        return message
             
    def check_webhook(self, webhook):
        try:
            with requests.get(webhook) as r:
                if r.status_code == 200:
                    return True
                else:
                    return False
        except:
            return False

    def print_message(self, message):
        self.textbox.insert(tk.END, message+'\n')
    
    def exit(self):
        self.print_message(f"{Fore.MAGENTA}Press anything to exit...{Fore.RESET}")
        self.textbox.configure(state='disabled')
        self.root.bind('<Return>', lambda event: self.root.destroy())

if __name__ == "__main__":
    init()
    
    if not os.name == "nt":
        os.system("clear")
    else:
        os.system("cls")
    
    try: 
        WebhookSpam().start()
    except KeyboardInterrupt: 
        input(f"\n\n{Fore.YELLOW}KeyboardInterrupt: Exiting...{Fore.RESET}")
    except Exception as e: 
        input(f"\n\n{Fore.RED}Error: {e}{Fore.RESET}")
