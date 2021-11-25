#!/usr/bin/env python
import random
import requests
import tkinter as tk
from rich import print
from bs4 import BeautifulSoup

fontsize = 12
page = input("Enter Page :")
if not page:
    page = "artificial-intelligence-questions-answers"
print("Fetching data ...")
try:
    res = requests.get("https://www.sanfoundry.com/" + page)
except requests.exceptions.RequestException:
    print("Couldn't get data")
    quit()
print("Fetched data")
print("Now parsing ...")
soup = BeautifulSoup(res.content, 'lxml')

print("\nSome additional pages :\n")
for a_href in soup.find_all("a", href=True):
    if 'questions' in a_href['href']:
        print('\t' + a_href['href'].split('/')[-2])
print('\n')

content = soup.find('div', 'entry-content')
paras = content.findAll('p')
header = paras.pop(0).text
mcqs = []

for each in paras:
    if '?' not in each.text:
        continue
    try:
        answerid = each.span['id']
    except:
        print(each)
        break
    answer_div = content.find('div', id='target-'+answerid)
    each.span.decompose()
    question = each.text.split("\n")[0].split(".", 1)[-1].strip()
    options = [option.split(')', 1)[-1].strip()
               for option in each.text.split('\n')[1:] if option != '']
    answer = answer_div.text.split('\n', 1)[0].strip('Answer: ')
    explanation = answer_div.text.split('\n', 1)[1].strip()
    question_dict = {
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation
    }
    mcqs.append(question_dict)


print("\rDone ...")
random.shuffle(mcqs)
print(f"Got {len(mcqs)} mcqs of {header}")


window = tk.Tk()
window.title(header)
window.configure(bg='#2d2d2d')
window.geometry('400x350')

total = 0
right = 0
keys = ('h','j','k','l')

def check(event):
    update(option_lbls.index(event.widget))

def keypress(event):
    try:
        index = keys.index(event.char.lower())
        update(index)
    except ValueError:
        pass


def update(index):
    global total, right
    total += 1
    explain_lbl.configure(state='normal')
    explain_lbl.delete('1.0', tk.END)
    try:
        answer = ord(mcq['answer'].lower()) - 97
    except TypeError:
        explain_lbl.insert(tk.END, "Answer Unknown :")
        explain_lbl['bg']='#5d5d1d'
        explain_lbl.insert(tk.END, mcq['explanation'])
        explain_lbl.configure(state='disabled')
        return


    explain_lbl.insert(tk.END, mcq['explanation'])
    explain_lbl.configure(state='disabled')
    if index == answer:
        explain_lbl['bg']='#1d5d1d'
        right += 1
    else:
        explain_lbl['bg']='#5d1d1d'

def next_mcq(*event):
    global mcq
    try:
        mcq = mcqs.pop(0)
    except IndexError:
        window.destroy()
        return

    explain_lbl.configure(state='normal')
    question_lbl.configure(state='normal')
    explain_lbl.delete('1.0', tk.END)
    question_lbl.delete('1.0', tk.END)
    question_lbl.insert(tk.END, mcq["question"])
    explain_lbl.configure(state='disabled')
    question_lbl.configure(state='disabled')
    explain_lbl['bg']='#2d2d2d'
    for option, lbl in zip(mcq["options"], option_lbls):
        lbl['text'] = option


question_lbl = tk.Text(window,
                     font=(None, fontsize),
                     fg='#d2d2d2',
                     bg='#1d1dad',
                     width=72,
                     height=5,
                     wrap='word',
                     state='disabled'
                     )

question_lbl.pack(padx=10, pady=10, fill=tk.X)

option_lbl_args =dict(font=(None, fontsize),
        fg='#d2d2d2',
        bg='#5d5d1d'
        )

option_lbls = [ tk.Label(window, **option_lbl_args) for i in range(4) ]
for lbl in option_lbls:
    lbl.pack(padx=10, pady=8)
    lbl.bind('<Button-1>',check)

explain_lbl = tk.Text(window,
			 bg='#2d2d2d',
			 font=(None, fontsize),
			 wrap='word',
			 state='disabled',
			 width=72,
                         height=10
             )

explain_lbl.pack(fill=tk.X)
question_lbl.bind('<Button-1>', next_mcq)
window.bind('<Return>', next_mcq)
for key in keys:
    window.bind(key, keypress)
next_mcq()

window.mainloop()
try:
    print(f"Accuracy : {round(right / total, 2) * 100}%")
except ZeroDivisionError:
    print("Not played!")
