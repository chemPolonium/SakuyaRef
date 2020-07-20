# coding: utf8
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import bibtexparser
from ctypes import windll
import shutil
import os
import pyperclip

paperlib_dir = "C:\\Users\\polonium\\OneDrive\\论文库"
bibfile_name = "mylib.bib"

with open(os.path.join(paperlib_dir, bibfile_name),
          encoding="utf-8") as bib_file:
    bib_database = bibtexparser.load(bib_file)

bib_list = [(
    bib_item["ID"],
    bib_item["author"],
    bib_item["title"],
    bib_item.get("journal", ""),
    bib_item.get("year", ""),
) for bib_item in bib_database.entries]

windll.shcore.SetProcessDpiAwareness(1)

root = tk.Tk()
root.state("zoomed")
root.title("SakuyaRef")
root.update()
style = ttk.Style(root                                                                 )
style.configure("Treeview", rowheight=40)


def tree_sort_column(tv, col, reverse):
    tv_list = [(tv.set(k, col), k) for k in tv.get_children("")]
    tv_list.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (_, k) in enumerate(tv_list):
        tv.move(k, "", index)

    # reverse sort next time
    tv.heading(col, command=lambda: tree_sort_column(tv, col, not reverse))


def tree_heading_with_sort(self, col):
    self.heading(col,
                 text=col,
                 command=lambda _col=col: tree_sort_column(self, _col, False))


tree_header = ["ID", "author", "title", "journal", "year"]
tree_header_display = ["author", "title", "journal", "year"]
ttk.Treeview.heading_with_sort = tree_heading_with_sort
tree = ttk.Treeview(
    root,
    columns=tree_header,
    displaycolumns=tree_header_display,
    show="headings",
    height=50,
)
tree.heading_with_sort("author")
tree.column("author", width=int(0.25 * root.winfo_width()))
tree.heading_with_sort("title")
tree.column("title", width=int(0.45 * root.winfo_width()))
tree.heading_with_sort("journal")
tree.column("journal", width=int(0.25 * root.winfo_width()))
tree.heading_with_sort("year")
tree.column("year", width=int(0.05 * root.winfo_width()), anchor="center")

for bib_item in bib_list:
    tree.insert("", "end", values=bib_item)
tree.pack(fill="both", expand=True)


def bind_pdf():
    print(tree.set(tree.selection(), "ID"), "bind pdf")
    bindfile_name = filedialog.askopenfilename()
    if len(bindfile_name) != 0:
        shutil.copyfile(
            bindfile_name,
            os.path.join(paperlib_dir,
                         tree.set(tree.selection(), "ID") + ".pdf"),
        )


def view_pdf(*event):
    print(tree.set(tree.selection(), "ID"), "view pdf")
    os.system("start " +
              os.path.join(paperlib_dir,
                           tree.set(tree.selection(), "ID") + ".pdf"))


def clear_bind():
    print(tree.set(tree.selection(), "ID"), "clear bind")
    os.remove(
        os.path.join(paperlib_dir,
                     tree.set(tree.selection(), "ID") + ".pdf"))


def delete_entry():
    print(tree.set(tree.selection(), "ID"), "delete entry")


def delete_entry_multi():
    for item in tree.selection():
        print(tree.set(item, "ID"), "delete entry")


def copy_title():
    pyperclip.copy(tree.set(tree.selection(), "title"))


menu_on_single = tk.Menu(root, tearoff=0)
menu_on_single.add_command(label="bind pdf", command=bind_pdf)
menu_on_single.add_command(label="view pdf", command=view_pdf)
menu_on_single.add_command(label="copy title", command=copy_title)
menu_on_single.add_command(label="clear bind", command=clear_bind)
menu_on_single.add_command(label="delete", command=delete_entry)

menu_on_multi = tk.Menu(root, tearoff=0)
menu_on_multi.add_command(label="clear bind", command=clear_bind)
menu_on_multi.add_command(label="delete", command=delete_entry_multi)


def popup(event):
    # select row under mouse
    iid = tree.identify_row(event.y)
    if iid:
        if iid not in tree.selection():
            tree.selection_set(iid)
        if len(tree.selection()) == 1:
            menu_on_single.post(event.x_root, event.y_root)
        else:
            menu_on_multi.post(event.x_root, event.y_root)
    else:
        pass


tree.bind("<Button-3>", popup)
tree.bind("<Return>", view_pdf)
tree.bind("<Double-Button-1>", view_pdf)

root.mainloop()
