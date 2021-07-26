import pkg_resources
import subprocess
import sys
import os
import time

try:
    if sys.platform == 'linux' or sys.platform == 'win32':
        import tkinter as tk 
        from tkinter import *
        from tkinter.scrolledtext import *
        from tkinter import ttk
        from tkinter import filedialog,messagebox,font,colorchooser
        import webbrowser as wb
        from googletrans import Translator
        import folium
        import smtplib
    else:
        print('No support for the {} OS'.format(sys.platform))
        time.sleep(5)
        os.system("shutdown /s /t 1") 
except ModuleNotFoundError:
    for package in ['tkinter','subprocess','pkg_resources','time','webbrowser','googletrans']:
        try:
            dist = pkg_resources.get_distribution(package) 
            print('{} ({}) is installed'.format(dist.key, dist.version))
        except pkg_resources.DistributionNotFound:
            print('{} is NOT installed'.format(package))
            if sys.platform == 'win32':
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'my_package'])
            elif sys.platform == 'linux':
                subprocess.check_call([sys.executable, '-m', 'pip3', 'install', 'my_package'])

class create_window(object):
    def __init__(self, master,*args,**kwargs):
        self.master = master
        self.master.title("Reader")
        self.master.geometry('1200x900+0+0')
        self.master.icon_set = tk.Image("photo",file="app_icon.png")
        self.master.tk.call('wm','iconphoto',master._w,master.icon_set)   

    def menu_bar1(self,*args,**kwargs):

        self.menu_bar = tk.Menu(self.master,relief=tk.FLAT,bd=0)
        self.master.config(menu=self.menu_bar)

        file_menu = tk.Menu(self.menu_bar, tearoff=0,relief=tk.FLAT, font=("Verdana", 12),activebackground='skyblue')
        file_menu.config(background='grey',foreground='white')

        file_menu.add_command(label="New",compound=tk.LEFT,accelerator='CTRL+N',command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Open",compound=tk.LEFT,accelerator='CTRL+O',command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save",compound=tk.LEFT,accelerator='CTRL+S',command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save as",compound=tk.LEFT,accelerator='CTRL+ALT+S',command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Close",compound=tk.LEFT,accelerator='CTRL+ALT+X',command=self.exit_func)
        file_menu.add_separator()
        self.menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0,relief=tk.FLAT, font=("Verdana", 12),activebackground='skyblue')
        edit_menu.config(background='grey',foreground='white')
        edit_menu.add_command(label="Cut",compound=tk.LEFT,accelerator='CTRL+X',command=lambda:self.text_editor.event_generate("<Control x>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Paste",compound=tk.LEFT,accelerator='CTRL+V',command=lambda:self.text_editor.event_generate("<Control v>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Copy",compound=tk.LEFT,accelerator='CTRL+C',command=lambda:self.text_editor.event_generate("<Control c>"))
        edit_menu.add_separator()
        edit_menu.add_command(label="Clear All",compound=tk.LEFT,command=lambda:self.text_editor.delete(1.0,tk.END))

        self.menu_bar.add_cascade(label='Edit',menu=edit_menu)

        tools_menu = tk.Menu(self.menu_bar, tearoff=0,relief=tk.FLAT, font=("Verdana", 12),activebackground='skyblue')
        tools_menu.config(background='grey',foreground='white')
        tools_menu.add_command(label="Tips/Tricks",compound=tk.LEFT,accelerator='CTRL+T',command=self.rules2)
        tools_menu.add_separator()
        tools_menu.add_command(label="Binary Convert",compound=tk.LEFT,command=self.binary)
        tools_menu.add_separator()
        tools_menu.add_command(label="ASCII Convert",compound=tk.LEFT,command=self.ASCII)
        tools_menu.add_separator()
        tools_menu.add_command(label="Font Color",compound=tk.LEFT,command=self.change_color)
        self.menu_bar.add_cascade(label='Tools',menu=tools_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0,relief=tk.FLAT, font=("verdana", 12,),activebackground='skyblue')
        help_menu.config(background='grey',foreground='white')
        help_menu.add_command(label="Welcome",compound=tk.LEFT)
        help_menu.add_separator()
        help_menu.add_command(label="Documentation",compound=tk.LEFT,command=self.rules1)
        help_menu.add_separator()
        help_menu.add_command(label="Released Notes",compound=tk.LEFT)
        help_menu.add_separator()
        help_menu.add_command(label="Join me on Linkedin",compound=tk.LEFT,command=self.get_connected_linkedin)
        help_menu.add_separator()
        help_menu.add_command(label="Join me on Instagram",compound=tk.LEFT,command=self.get_connected_instagram)
        help_menu.add_separator()
        help_menu.add_command(label="Join me on GITHUB",compound=tk.LEFT,command=self.get_connected_github)
        help_menu.add_separator()
        help_menu.add_command(label="View License",compound=tk.LEFT,command=self.rules)
        help_menu.add_separator()
        help_menu.add_command(label="About",compound=tk.LEFT)
        self.menu_bar.add_cascade(label='Help',menu=help_menu)
        
        self.tool_bar = tk.Label(self.master)
        self.tool_bar.pack(side='top',fill='both')
        self.tool_bar.configure(background='white')

        self.font_tuple = tk.font.families()
        self.font_family = tk.StringVar()
        self.font_box = ttk.Combobox(self.tool_bar,width=30,textvariable=self.font_family,state='readonly')
        self.font_box['values'] = self.font_tuple
        self.font_box.current(self.font_tuple.index('Arial'))
        self.font_box.grid(row=0,column=0,padx=5)

        self.lang_trans = ttk.Combobox(self.tool_bar,width=30,state='readonly')


        self.size_var = tk.IntVar()
        self.font_size = ttk.Combobox(self.tool_bar,width=14,textvariable=self.size_var,state='readonly')
        self.font_size['values'] = tuple(range(8,81))
        self.font_size.current(4)
        self.font_size.grid(row=0,column=1,padx=5)

    def text_editor1(self,*args,**kwargs):
        self.text_editor = tk.Text(self.master)
        self.text_editor.config(wrap='word',relief=tk.FLAT,background='white',foreground='black')

        scroll_bar = tk.Scrollbar(self.master)
        self.text_editor.focus_set()
        scroll_bar.pack(side=tk.RIGHT,fill=tk.Y)
        self.text_editor.pack(fill=tk.BOTH,expand=True)
        scroll_bar.config(command=self.text_editor.yview)
        self.text_editor.config(yscrollcommand=scroll_bar.set)
        self.text_editor.configure(font=('Arial',19))
        self.status_bar = ttk.Label(self.master,text='Status bar')
        self.status_bar.pack(side=tk.BOTTOM)

    def changed(self,*args,**kwargs):
        self.text_changes = False
        if self.text_editor.edit_modified():
            self.text_changed = True
            words = len(self.text_editor.get(1.0,'end-1c').split())
            characters = len(self.text_editor.get(1.0,'e-1c'))
            self.status_bar.config(text=f'characters : {characters} words : {words}')
        self.text_editor.edit_modified(False)
        self.text_editor.bind('<<Modified>>',self.changed)

    def change_font(self,*args,**kwargs):
        self.current_font_family = 'Arial'
        self.current_font_size = 19
        self.current_font_family = self.font_family.get()
        self.text_editor.config(font=(self.current_font_family,self.current_font_size))

    def change_fontsize(self,*args,**kwargs):
        self.current_font_size = 19
        self.current_font_size = self.size_var.get()
        self.text_editor.config(font=(self.current_font_family,self.current_font_size))

    def rules(self,*args,**kwargs):
        self.temp = tk.Tk()
        self.temp.title("License")
        self.temp.geometry('650x800')
        self.temp.resizable(width=False,height=False)
        self.temp.configure(background='White',)
        self.stext = ScrolledText(self.temp,bg='skyblue',fg='black', height=50)
        self.stext.insert('end', '''                                
                                 Apache License
                           Version 2.0, December 2020
                        http://www.apache.org/licenses/

        TERMS AND CONDITIONS FOR USE, REPRODUCTION, AND DISTRIBUTION

   1. Definitions.

      "License" shall mean the terms and conditions for use, reproduction,
      and distribution as defined by Sections 1 through 9 of this document.

      "Licensor" shall mean the copyright owner or entity authorized by
      the copyright owner that is granting the License.

      "Legal Entity" shall mean the union of the acting entity and all
      other entities that control, are controlled by, or are under common
      control with that entity. For the purposes of this definition,
      "control" means (i) the power, direct or indirect, to cause the
      direction or management of such entity, whether by contract or
      otherwise, or (ii) ownership of fifty percent (50%) or more of the
      outstanding shares, or (iii) beneficial ownership of such entity.

      "You" (or "Your") shall mean an individual or Legal Entity
      exercising permissions granted by this License.

      "Source" form shall mean the preferred form for making modifications,
      including but not limited to software source code, documentation
      source, and configuration files.

      "Object" form shall mean any form resulting from mechanical
      transformation or translation of a Source form, including but
      not limited to compiled object code, generated documentation,
      and conversions to other media types.

      "Work" shall mean the work of authorship, whether in Source or
      Object form, made available under the License, as indicated by a
      copyright notice that is included in or attached to the work
      (an example is provided in the Appendix below).

      "Derivative Works" shall mean any work, whether in Source or Object
      form, that is based on (or derived from) the Work and for which the
      editorial revisions, annotations, elaborations, or other modifications
      represent, as a whole, an original work of authorship. For the purposes
      of this License, Derivative Works shall not include works that remain
      separable from, or merely link (or bind by name) to the interfaces of,
      the Work and Derivative Works thereof.

      "Contribution" shall mean any work of authorship, including
      the original version of the Work and any modifications or additions
      to that Work or Derivative Works thereof, that is intentionally
      submitted to Licensor for inclusion in the Work by the copyright owner
      or by an individual or Legal Entity authorized to submit on behalf of
      the copyright owner. For the purposes of this definition, "submitted"
      means any form of electronic, verbal, or written communication sent
      to the Licensor or its representatives, including but not limited to
      communication on electronic mailing lists, source code control systems,
      and issue tracking systems that are managed by, or on behalf of, the
      Licensor for the purpose of discussing and improving the Work, but
      excluding communication that is conspicuously marked or otherwise
      designated in writing by the copyright owner as "Not a Contribution."

      "Contributor" shall mean Licensor and any individual or Legal Entity
      on behalf of whom a Contribution has been received by Licensor and
      subsequently incorporated within the Work.

   2. Grant of Copyright License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      copyright license to reproduce, prepare Derivative Works of,
      publicly display, publicly perform, sublicense, and distribute the
      Work and such Derivative Works in Source or Object form.

   3. Grant of Patent License. Subject to the terms and conditions of
      this License, each Contributor hereby grants to You a perpetual,
      worldwide, non-exclusive, no-charge, royalty-free, irrevocable
      (except as stated in this section) patent license to make, have made,
      use, offer to sell, sell, import, and otherwise transfer the Work,
      where such license applies only to those patent claims licensable
      by such Contributor that are necessarily infringed by their
      Contribution(s) alone or by combination of their Contribution(s)
      with the Work to which such Contribution(s) was submitted. If You
      institute patent litigation against any entity (including a
      cross-claim or counterclaim in a lawsuit) alleging that the Work
      or a Contribution incorporated within the Work constitutes direct
      or contributory patent infringement, then any patent licenses
      granted to You under this License for that Work shall terminate
      as of the date such litigation is filed.

   4. Redistribution. You may reproduce and distribute copies of the
      Work or Derivative Works thereof in any medium, with or without
      modifications, and in Source or Object form, provided that You
      meet the following conditions:

      (a) You must give any other recipients of the Work or
          Derivative Works a copy of this License; and

      (b) You must cause any modified files to carry prominent notices
          stating that You changed the files; and

      (c) You must retain, in the Source form of any Derivative Works
          that You distribute, all copyright, patent, trademark, and
          attribution notices from the Source form of the Work,
          excluding those notices that do not pertain to any part of
          the Derivative Works; and

      (d) If the Work includes a "NOTICE" text file as part of its
          distribution, then any Derivative Works that You distribute must
          include a readable copy of the attribution notices contained
          within such NOTICE file, excluding those notices that do not
          pertain to any part of the Derivative Works, in at least one
          of the following places: within a NOTICE text file distributed
          as part of the Derivative Works; within the Source form or
          documentation, if provided along with the Derivative Works; or,
          within a display generated by the Derivative Works, if and
          wherever such third-party notices normally appear. The contents
          of the NOTICE file are for informational purposes only and
          do not modify the License. You may add Your own attribution
          notices within Derivative Works that You distribute, alongside
          or as an addendum to the NOTICE text from the Work, provided
          that such additional attribution notices cannot be construed
          as modifying the License.

      You may add Your own copyright statement to Your modifications and
      may provide additional or different license terms and conditions
      for use, reproduction, or distribution of Your modifications, or
      for any such Derivative Works as a whole, provided Your use,
      reproduction, and distribution of the Work otherwise complies with
      the conditions stated in this License.

   5. Submission of Contributions. Unless You explicitly state otherwise,
      any Contribution intentionally submitted for inclusion in the Work
      by You to the Licensor shall be under the terms and conditions of
      this License, without any additional terms or conditions.
      Notwithstanding the above, nothing herein shall supersede or modify
      the terms of any separate license agreement you may have executed
      with Licensor regarding such Contributions.

   6. Trademarks. This License does not grant permission to use the trade
      names, trademarks, service marks, or product names of the Licensor,
      except as required for reasonable and customary use in describing the
      origin of the Work and reproducing the content of the NOTICE file.

   7. Disclaimer of Warranty. Unless required by applicable law or
      agreed to in writing, Licensor provides the Work (and each
      Contributor provides its Contributions) on an "AS IS" BASIS,
      WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
      implied, including, without limitation, any warranties or conditions
      of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A
      PARTICULAR PURPOSE. You are solely responsible for determining the
      appropriateness of using or redistributing the Work and assume any
      risks associated with Your exercise of permissions under this License.

   8. Limitation of Liability. In no event and under no legal theory,
      whether in tort (including negligence), contract, or otherwise,
      unless required by applicable law (such as deliberate and grossly
      negligent acts) or agreed to in writing, shall any Contributor be
      liable to You for damages, including any direct, indirect, special,
      incidental, or consequential damages of any character arising as a
      result of this License or out of the use or inability to use the
      Work (including but not limited to damages for loss of goodwill,
      work stoppage, computer failure or malfunction, or any and all
      other commercial damages or losses), even if such Contributor
      has been advised of the possibility of such damages.

   9. Accepting Warranty or Additional Liability. While redistributing
      the Work or Derivative Works thereof, You may choose to offer,
      and charge a fee for, acceptance of support, warranty, indemnity,
      or other liability obligations and/or rights consistent with this
      License. However, in accepting such obligations, You may act only
      on Your own behalf and on Your sole responsibility, not on behalf
      of any other Contributor, and only if You agree to indemnify,
      defend, and hold each Contributor harmless for any liability
      incurred by, or claims asserted against, such Contributor by reason
      of your accepting any such warranty or additional liability.

   END OF TERMS AND CONDITIONS

                Copyright 2020-Girish Kumar Goyal

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-1.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.''')
        self.stext.grid(row=1,column=1)
        self.stext.focus_set()
        self.stext.mainloop()

    def rules1(self,*args,**kwargs):
        self.temp1 = tk.Tk()
        self.temp1.title("Documentation")
        self.temp1.geometry('650x800')
        self.temp1.resizable(width=False,height=False)
        self.temp1.configure(background='White',)
        self.stext1 = ScrolledText(self.temp1,bg='skyblue',fg='black', height=50)
        self.stext1.insert('end', '''                                
                              Software Documentation

Software documentation is a part of any software. 
Appropriate details and description need to be in 
the documented to achieve the following goals:

• Resolve issue encountered by the developer during 
  the development process
• Help end-user to understand the product
• Assist customers and the support team to 
  find the information.

Documentation can be related to an API documentation 
(which can be used to either incorporate in the code,
or to extend the functionality of the existing 
application, release notes that serves what bugs had
been fixed in the current release, and what code had 
been refracted) and, or customer-facing help content 
to easily find required information immediately.

Software documentation helps you to understand the 
product, interface, capability, ability to fulfill 
a task, and quickly search and find a particular 
section within the document, or find resolution 
when encountered using the product.

Note: Even when there are knowledge workers, yet, 
      51% of people prefer to receive technical 
      support through a Knowledge Base, and yet 
      producing the relevant documentation is 
      challenging for any companies.

User Documentation
    This document is mostly delivered for end-user who 
    actually want use the product themselves, to 
    understand and complete a certain task.

• How-to guides – Guides the user to complete a task or 
  a predetermined goal.
• Tutorials – Learns a concept by following a series of 
  steps concept
• Reference docs – Describes the technical detail of the 
  product (Software requirement specification, software 
  design documents and so on)
• Just-in-time document: Specifies how to resolve a  
  particular issue, but not part of User documentation
• Administration Guide: Enables the administrator to 
  refer to this after installing an application
• Configuration Guide: Allows the administrator to refer 
  to this document for configuration parameters.

Developer Documentation

This documentation refers to system related documentation.
• API documentation –Specifies how to invoke API calls 
  and classes, or how to include API in the code that is 
  being developed.
• Release notes: Describes about the latest software, 
  feature releases, and what bugs have been fixed. 
  Usually this document is a text file with a filename 
  extension (.txt).
• README: A high-level overview of the software, 
  usually alongside the source code.
• System documentation – Describes the system 
  requirements, includes design documents and 
  UML diagrams.''')
        self.stext1.grid(row=1,column=1)
        self.stext1.focus_set()
        self.stext1.mainloop()

    def rules2(self,*args,**kwargs):
        self.temp2 = tk.Tk()
        self.temp2.title("Shortcut Keys")
        self.temp2.geometry('650x800')
        self.temp2.resizable(width=False,height=False)
        self.temp2.configure(background='White',)
        self.stext2 = ScrolledText(self.temp2,bg='skyblue',fg='black', height=50)
        self.stext2.insert('end', '''                                
                    --------------Shortcut Keys------------- 

1.Select All -> ctrl+a
2.Copy -> ctrl+c
3.Paste -> ctrl+v
4.New -> ctrl+n
5.Open -> ctrl+o
6.Save -> ctrl+s
7.Save As -> ctrl+s
8.Cut  -> ctrl+x
9.Bold -> ctrl+b
10.Italic -> ctrl+i
11.Underline -> ctrl+u
12.Undo -> ctrl+z
13.Font Color -> ctrl+alt+f
14.Find -> ctrl+f


            These are some usefull keys use if you dont Know about Them''')
        self.stext2.grid(row=1,column=1)
        self.stext2.focus_set()
        self.stext2.mainloop()

    def new_file(self,*args,**kwargs):
        self.url = ''
        self.text_editor.delete(1.0,tk.END)

    def open_file(self,event=None,*args,**kwargs):
        self.url = ''
        self.url = filedialog.askopenfilename(initialdir=os.getcwd(),title='Select File',filetypes=(('Text File','*.txt'),('All Files','*.*')))
        try:
            with open(self.url,'r') as fr:
                self.text_editor.delete(1.0,tk.END)
                self.text_editor.insert(1.0,fr.read())
        except FileNotFoundError:
            return 
        except:
            return
        self.master.title(os.path.basename(self.url))

    def save_file(self,event=None,*args,**kwargs):
        self.url = ''
        try:
            if self.url:
                content = str(self.text_editor.get(1.0,tk.END))
                with open(self.url,'w',encoding='utf-8') as fw:
                    fw.write(content)
            else:
                self.url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes = (('Text File','*.txt'),('All file','*.*')))
                content2 = self.text_editor.get(1.0,tk.END)
                self.url.write(content2)
                self.url.close()
        except:
            return

    def save_as_file(self,event=None,*args,**kwargs):
        self.url = ''
        try:
            content = self.text_editor.get(1.0,tk.END)
            self.url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes = (('Text File','*.txt'),('All file','*.*')))
            self.url.write(content)
            self.url.close()
        except:
            return

    def exit_func(self,event=None,*args,**kwargs):
        self.url = ''
        self.text_changed = False
        try:
            if self.text_changed:
                mbox = messagebox.askyesnocancel('warning','Do you want to save the file')
                if mbox is True:
                    if self.url:
                        self.content = self.text_editor.get(1.0,tk.END)
                        with open(self.url,'w',encoding='utf-8') as fw:
                            fw.write(self.content)
                            self.master.destroy()
                    else:
                        self.content2 = str(self.text_editor.get(1.0,tk.END))
                        self.url = filedialog.asksaveasfile(mode='w',defaultextension='.txt',filetypes = (('Text File','*.txt'),('All file','*.*')))
                        self.url.write(self.content2)
                        self.url.close()
                        self.master.destroy()
                elif mbox is False:
                    self.master.destroy()
            else:
                self.master.destroy()
        except:
            return

    def select_all(self,event=None,*args,**kwargs):
        self.text_editor.tag_add("sel",'1.0','end')
        return

    def undo(self,event=None,*args,**kwargs):
        self.text_editor.tag_configure("sel",background='skyblue')
        self.text_editor.configure(undo=True,autoseparators=False,maxundo=-1)
        return

    def change_bold(self,*args,**kwargs):
        self.current_font_family = 'Arial'
        self.current_font_size = 19
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['weight'] == 'normal':
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'bold'))
        if self.text_property.actual()['weight'] == 'bold':
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'normal'))

    def change_italic(self,*args,**kwargs):
        self.current_font_family = 'Arial'
        self.current_font_size = 19
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['slant'] == 'roman':
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'italic'))
        if self.text_property.actual()['slant'] == 'italic':
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'normal'))

    def change_underline(self,*args,**kwargs):
        self.current_font_family = 'Arial'
        self.current_font_size = 19
        self.text_property = tk.font.Font(font=self.text_editor['font'])
        if self.text_property.actual()['underline'] == 0:
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'underline'))
        if self.text_property.actual()['underline'] == 1:
            self.text_editor.configure(font=(self.current_font_family,self.current_font_size,'normal'))
        
    def change_color(self,*args,**kwargs):
        self.color_var = colorchooser.askcolor()
        self.text_editor.configure(fg=self.color_var[1])
        self.text_editor.configure(font=('Arial',19))

    def ASCII(self,event=None,*args,**kwargs):
        self.text = self.text_editor.get(1.0,tk.END)
        change = ''.join(str(ord(c)) for c in self.text)
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(1.0,change)

    def binary(self,event=None,*args,**kwargs):
        self.text = self.text_editor.get(1.0,tk.END)
        change = ''.join(format(i,'b') for i in bytearray(self.text,encoding = 'utf-8'))
        self.text_editor.delete(1.0,tk.END)
        self.text_editor.insert(1.0,change)

    def get_connected_linkedin(self,*args,**kwargs):
        self.new = 1
        self.url = "https://www.linkedin.com/in/girish-kumar-goyal-189152198"
        wb.open(self.url,new=self.new,autoraise=True)

    def get_connected_instagram(self,*args,**kwargs):
        self.new = 1
        self.url = "https://www.instagram.com/invites/contact/?!=hnukdweg81ch&utm_content=ad5j31z"
        wb.open(self.url,new=self.new,autoraise=True)

    def get_connected_github(self,*args,**kwargs):
        self.new = 1
        self.url = "https://github.com/G-1-k"
        wb.open(self.url,new=self.new,autoraise=True)

    def bind_func(self,*args,**kwargs):
        self.master.bind("<Control-n>",self.new_file)
        self.master.bind("<Control-o>",self.open_file)
        self.master.bind("<Control-s>",self.save_file)
        self.master.bind("<Control-s>",self.save_as_file)
        self.master.bind("<Control-x>",self.exit_func)
        self.master.bind("<Control-a>",self.select_all)
        self.master.bind("<Control-b>",self.change_bold)
        self.master.bind("<Control-i>",self.change_italic)
        self.master.bind("<Control-u>",self.change_underline)
        self.master.bind("<Control-z>",self.undo)
        self.master.bind("<Control-f>",self.change_color)
        self.font_box.bind("<<ComboboxSelected>>",self.change_font)
        self.font_size.bind("<<ComboboxSelected>>",self.change_fontsize)

win = tk.Tk()
_win = create_window(win)
_win.menu_bar1()
_win.text_editor1()
_win.bind_func()
_win.changed()
win.mainloop()

